import sys
import logging
from tutorlist_api import rds_config
import pymysql
import json

# rds settings
rds_host = "flattenthecurve-mcc.cta6mutfcbyy.ap-southeast-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# executes upon API event
def handler(event, context):
    # connect using creds from rds_config.py
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

    # array to store values to be returned
    records = []
    with conn.cursor() as cur:
        cur.execute('select * from TUTOR AS T inner join ORGANISATION AS O on T.ORGANISATION_ID = O.ID')
        conn.commit()
        for row in cur:
            record = {
                'ID': row[0],
                'NAME': row[1],
                'PHONE': row[2],
                'ADDRESS': row[3],
                'TFN': row[4],
                'VERIFICATION_ID': row[5],
                'ORGANISATION_NAME': row[8],
                'ORGANISATION_STATE': row[9],
                'ORGANISATION_COUNTRY': row[10],
            }
            records.append(record)

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(records)

    return responseObject