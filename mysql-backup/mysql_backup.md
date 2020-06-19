# common documentation:
* https://dev.mysql.com/doc/refman/8.0/en/backup-and-recovery.html

## [dump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)

## [replication](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
* [replication solutions](https://dev.mysql.com/doc/refman/8.0/en/replication-solutions.html)
* [replication implementation](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation.html)
* [replication notes and tips](https://dev.mysql.com/doc/refman/8.0/en/replication-notes.html)
* [replication FAQ](https://dev.mysql.com/doc/refman/8.0/en/faqs-replication.html)
* [replicating to slaves](https://dev.mysql.com/doc/refman/8.0/en/replication-solutions-partitioning.html)

[backup policies](https://dev.mysql.com/doc/refman/8.0/en/backup-policy.html):
* dump
    * manual start and stop 
        * make the server ReadOnly
        ```bash
        mysql> FLUSH TABLES WITH READ LOCK;
        mysql> SET GLOBAL read_only = ON;
        ```
        * make dump
        * back server to Normal Mode
        ```bash
        mysql> SET GLOBAL read_only = OFF;
        mysql> UNLOCK TABLES;    
        ```
    * with one command without manual step
        * mysqldump --master-data --single-transaction > backup.sql
* dump tools
    * [ubuntu utility: automysqlbackup](https://www.digitalocean.com/community/tutorials/how-to-backup-mysql-databases-on-an-ubuntu-vps)
    * raw solution via cron
        ```
        crontab -e
        # And add the following config
        50 23 */2 * * mysqldump -u mysqldump DATABASE | gzip > dump.sql.gz >/dev/null 2>&1
        ```        
    * [raw to s3cmd (amazon, digitalocean...) ](https://www.danielord.co.uk/backup-mysql-database-digital-ocean-spaces)
* dump with binary log position
    ```bash
    # innodb
    mysqldump --single-transaction --flush-logs --master-data=2 --all-databases --delete-master-logs > backup.sql
    # not innodb
    mysqldump --lock-tables
    ```

    

## cold backup (raw files)
Cold Backups
If you can shut down the MySQL server, 
you can make a physical backup that consists of all files used by InnoDB to manage its tables. 
Use the following procedure:
* Perform a slow shutdown of the MySQL server and make sure that it stops without errors.
* Copy all InnoDB data files (ibdata files and .ibd files)
* Copy all InnoDB log files (ib_logfile files)
* Copy your my.cnf configuration file

# Digital Ocean managed solution
[How to add ReadOnly nodes](https://www.digitalocean.com/docs/databases/mysql/how-to/add-read-only-nodes/)
```
Read-only nodes are replicas of a cluster's primary node located in additional geographical regions. Using read-only nodes reduces latency for users connecting from those regions.
Communication between primary and read-only nodes is SSL-encrypted 
```

