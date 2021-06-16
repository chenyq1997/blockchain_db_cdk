import os
import sys
import logging
import MySQLdb  # TODO Error recognizing _mysql: switch back to PyMySQL
import boto3

# rds settings
rds_host = os.environ['db_endpoint_address']  # TODO
name = "admin"
password = "8fsB-F(('pQvK5eu"
db_name = "db1"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO Try connect DB here


def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'MySQLdb was successfully imported'
    }
