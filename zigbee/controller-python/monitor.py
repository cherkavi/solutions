
#!/usr/bin/env python3

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

import paho.mqtt.client as mqtt

DB = Path(__file__).parent / "sensors.db"

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "zigbee2mqtt/+"

@contextmanager
def db():
    conn = sqlite3.connect(DB)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensor_state (
                sensor_id TEXT PRIMARY KEY,
                contact INTEGER,
                battery INTEGER,
                last_seen TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensor_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT,
                event TEXT,
                timestamp TEXT
            )
        """)
        yield conn
        conn.commit()
    finally:
        conn.close()


def process_message(topic, payload, retained=False):
    sensor = topic.split("/")[-1]

    if sensor == "bridge" or sensor == "+":
        return

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return

    if "contact" not in data:
        return

    contact = bool(data["contact"])
    battery = data.get("battery")
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    with db() as conn:
        previous = conn.execute(
            "SELECT contact FROM sensor_state WHERE sensor_id=?",
            (sensor,)
        ).fetchone()

        conn.execute("""
            INSERT INTO sensor_state
                (sensor_id, contact, battery, last_seen)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(sensor_id) DO UPDATE SET
                contact=excluded.contact,
                battery=excluded.battery,
                last_seen=excluded.last_seen
        """, (sensor, int(contact), battery, now))

        # Do not treat MQTT retained messages as new events.
        if not retained and (
            previous is None or previous[0] != int(contact)
        ):
            event = "CLOSED" if contact else "OPENED"

            conn.execute("""
                INSERT INTO sensor_events
                    (sensor_id, event, timestamp)
                VALUES (?, ?, ?)
            """, (sensor, event, now))

            print(f"[{now}] {sensor}: {event}", flush=True)


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT:", reason_code)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    process_message(msg.topic, msg.payload.decode(), msg.retain)


def run():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="zigbee-monitor"
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)
    print("Monitoring Zigbee sensors...")
    client.loop_forever()


def status():
    with db() as conn:
        rows = conn.execute("""
            SELECT sensor_id, contact, battery, last_seen
            FROM sensor_state
            ORDER BY sensor_id
        """).fetchall()

    print(f"{'SENSOR':25} {'STATE':10} {'BATTERY':10} LAST SEEN")
    print("-" * 90)

    for sensor, contact, battery, seen in rows:
        state = "CLOSED" if contact else "OPEN"
        print(f"{sensor:25} {state:10} {str(battery):10} {seen}")


def history(sensor=None, limit=30):
    with db() as conn:
        if sensor:
            rows = conn.execute("""
                SELECT sensor_id, event, timestamp
                FROM sensor_events
                WHERE sensor_id=?
                ORDER BY id DESC LIMIT ?
            """, (sensor, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT sensor_id, event, timestamp
                FROM sensor_events
                ORDER BY id DESC LIMIT ?
            """, (limit,)).fetchall()

    for sensor_id, event, timestamp in rows:
        print(f"{timestamp} | {sensor_id:25} | {event}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Zigbee door/window monitoring"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("run")
    sub.add_parser("status")

    h = sub.add_parser("history")
    h.add_argument("--sensor")
    h.add_argument("--limit", type=int, default=30)

    args = parser.parse_args()

    if args.command == "run":
        run()
    elif args.command == "status":
        status()
    elif args.command == "history":
        history(args.sensor, args.limit)
