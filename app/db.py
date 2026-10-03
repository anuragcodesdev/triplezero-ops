import os
from  dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
    )
    return conn


def insert_incident(incident):
    conn = get_connection()
    cursor = conn.cursor()

    sql ="""
            INSERT INTO incidents (
            incident_type, 
            latitude, 
            longitude, 
            description,
            severity,
            status,
            reported_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    cursor.execute(
        sql,
        (
            incident.incident_type,
            incident.latitude,
            incident.longitude,
            incident.description,
            incident.severity,
            incident.status.value,
            incident.reported_at,
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_response_unit(response_unit):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
            INSERT into response_units (
            callsign,
            unit_type,
            status)
            VALUES (%s, %s, %s)
          """

    cursor.execute(
        sql,
        (
            response_unit.callsign,
            response_unit.unit_type,
            response_unit.status.value
         ),
    )
    conn.commit()
    cursor.close()
    conn.close()