import os
import sys
import logging
import pymysql
import boto3
import query_amberdata

# rds settings
rds_host = os.environ['db_endpoint_address']
name = "admin"
password = "8fsB-F(('pQvK5eu"
db_name = "db1"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host,
                           user=name,
                           password=password,
                           db=db_name,
                           connect_timeout=5,
                           cursorclass=pymysql.cursors.DictCursor)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

# amberdata query
results = query_amberdata.retrieve()
logger.info("Query successful.\n")

def handler(event, context):
    service()



def service():
    # TODO
    create_table = "CREATE TABLE IF NOT EXISTS `records` ( \
                                        `id` INT(11) NOT NULL AUTO_INCREMENT, \
                                        `address_from` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `address_to` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `amount` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `blockHash` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `blockNumber` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `decimals` INT(11) COLLATE utf8_bin NOT NULL, \
                                        `name` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `symbol` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `timestamp` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `tokenAddress` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `transactionHash` VARCHAR(255) COLLATE utf8_bin NOT NULL, \
                                        `isERC20` BOOLEAN, \
                                        PRIMARY KEY (`id`) \
                                        ) \
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin \
                            AUTO_INCREMENT=1 ; "

    with conn.cursor() as cur:
        cur.execute(create_table)
        conn.commit()

    logger.info("Create/check table successful. \n")
    '''
    item_count = 0
    for result in results:
        with conn.cursor() as cur:
            cur.execute("create table Employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
            cur.execute('insert into Employee (EmpID, Name) values(1, "Joe")')
            cur.execute('insert into Employee (EmpID, Name) values(2, "Bob")')
            cur.execute('insert into Employee (EmpID, Name) values(3, "Mary")')
            conn.commit()

        conn.commit()

    logger.info("Added %d items to RDS MySQL table" % item_count)
    '''
