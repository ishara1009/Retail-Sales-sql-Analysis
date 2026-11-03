"""MySQL connection configuration."""

import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfigError(ValueError):
    """Raised when required database settings are missing or invalid."""


def get_connection():
    """Open and return a configured MySQL connection."""
    required = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise DatabaseConfigError(
            "Missing database settings: " + ", ".join(missing) + ". Copy .env.example to .env and edit it."
        )
    try:
        port = int(os.environ["MYSQL_PORT"])
    except ValueError as error:
        raise DatabaseConfigError("MYSQL_PORT must be a number.") from error
    try:
        return mysql.connector.connect(
            host=os.environ["MYSQL_HOST"], port=port, user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"], database=os.environ["MYSQL_DATABASE"],
        )
    except Error as error:
        raise ConnectionError(
            "Could not connect to MySQL. Check that MySQL is running, the database exists, and .env is correct. "
            f"MySQL says: {error}"
        ) from error
