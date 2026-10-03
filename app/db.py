import os
from typing import Any

from dotenv import load_dotenv
import psycopg2

from app.models import Incident, ResponseUnit

load_dotenv()

def get_connection() -> Any:
    """
    Creates a database connection from the environment configuration. This keeps the app code consistent and avoids repeating database connection setup.

    params:
        :None None: No parameters are required.
    returns:
        :conn connection: A configured PostgreSQL connection object.
    """
    conn: Any = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return conn


def insert_incident(incident: Incident) -> None:
    """
    Stores a new incident record in the database. It writes each field from the provided incident object and commits the transaction immediately.

    params:
        :incident incident: An Incident model instance containing the incident details to store.
    returns:
        :None None: This function does not return a value.
    """
    conn: Any = get_connection()
    cursor: Any = conn.cursor()

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

def insert_response_unit(response_unit: ResponseUnit) -> None:
    """
    Adds a response unit entry to the database. It writes the unit details and saves the record in one transaction.

    params:
        :response_unit response_unit: A ResponseUnit model instance containing the unit data to store.
    returns:
        :None None: This function does not return a value.
    """
    conn: Any = get_connection()
    cursor: Any = conn.cursor()

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
            response_unit.status.value,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()