import os
from typing import Any, List

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from app.models import Incident, ResponseUnit, IncidentOut


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
    cursor: Any = conn.cursor(cursor_factory=RealDictCursor)

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
            RETURNING id
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

    data = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return data['id']

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


def get_all_incidents() -> list[Incident]:
    """
    Fetches every incident record from the database. It converts each row into an Incident model so the calling code can work with typed objects.

    params:
        :None None: No parameters are required.
    returns:
        :incidents list: A list of Incident objects loaded from the database.
    """
    conn: Any = get_connection()
    cursor: Any = conn.cursor(cursor_factory=RealDictCursor)

    sql: str = """SELECT * FROM INCIDENTS;"""

    cursor.execute(sql)
    data: list[dict[str, Any]] = cursor.fetchall()

    cursor.close()
    conn.close()

    incidents: list[Incident] = []
    for row in data:
        incident_obj: Incident = Incident.model_validate(row)
        incidents.append(incident_obj)

    return incidents

def get_incident(id: int) -> IncidentOut:
    conn : Any = get_connection()
    cursor : Any = conn.cursor(cursor_factory = RealDictCursor)


    sql: str = """
        SELECT *
        FROM incidents
        WHERE id = %s;
    """

    cursor.execute(sql, (id,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data
     
