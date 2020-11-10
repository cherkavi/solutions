variable "MYSQL_HOST" {}
variable "MYSQL_PORT" {}
variable "MYSQL_USER" {}
variable "MYSQL_PASSWORD" {}
variable "MYSQL_DATABASE" {}
variable "USER_DB_REACT_BRIDGE_NAME" {}
variable "USER_DB_REACT_BRIDGE_PASS" {}

provider "mysql" {
  endpoint = "${var.MYSQL_HOST}:${var.MYSQL_PORT}"
  username = var.MYSQL_USER
  password = var.MYSQL_PASSWORD
}

resource "mysql_user" "user_db_react" {
    user = var.USER_DB_REACT_BRIDGE_NAME
    host = "%"
    plaintext_password = var.USER_DB_REACT_BRIDGE_PASS
}

resource "mysql_grant" "user_db_react_listing_associations" {
  user       = var.USER_DB_REACT_BRIDGE_NAME
  host       = "%"
  database   = var.MYSQL_DATABASE
  table = "listing_associations"
  privileges = ["SELECT"]
}
