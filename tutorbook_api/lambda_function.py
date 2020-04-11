import sys
import logging
from tutorbook_api import rds_config
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


def lambda_handler(event, context):
    # connect using creds from rds_config.py
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

    guardian_id = event['queryStringParameters']['guardianID']
    tutor_id = event['queryStringParameters']['tutorID']
    organisation_id = event['queryStringParameters']['organisationID']
    datetime = event['queryStringParameters']['datetime']
    session_name = event['queryStringParameters']['sessionName']
    conference_url = event['queryStringParameters']['confURL']
    student_id = event['queryStringParameters']['studentID']

    with conn.cursor() as cur:
        cur.execute('SESSION ("NAME", "COST", "ORGANISATION_ID", "GUARDIAN_ID", "TUTOR_ID", "Date", "STUDENT_ID") VALUES ("'+str(session_name)+'", "20", "'+str(organisation_id)+'", "'+str(guardian_id)+'", "'+str(tutor_id)+'"'+', ' + str(datetime)  + ', "'+str(student_id)+'");')
        conn.commit()

    return {
        'statusCode': 200,
        'body': json.dumps('Inserted Succesfully')
    }
