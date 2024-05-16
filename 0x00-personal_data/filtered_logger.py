#!/usr/bin/env python3
"""
Module that has many functions that deals with personal data.
"""


from datetime import datetime
import logging
from mysql.connector import connection
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate fields from a log string """
    for field in fields:
        match = re.search(rf'{field}=(.*?){separator}', message)
        if match:
            message = re.sub(match.group(1), redaction, message, 1)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init function """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the LogRecord """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ Function that creates a logger """
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data = logging.getLogger('user_data')
    user_data.propagate = False
    user_data.setLevel(logging.INFO)
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> connection.MySQLConnection:
    """ Function that creates a connector for the database """
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    if host is None:
        host = "localhost"
    user = os.getenv("PERSONAL_DATA_DB_USERNAME")
    if user is None:
        user = "root"
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    if pwd is None:
        pwd = ""
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    db_connection = connection.MySQLConnection(
        user=user, password=pwd,
        host=host, database=database
    )
    return db_connection


def main():
    """ Main function """
    db_connection = get_db()
    logger = get_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        pii = []
        for data in row:
            if isinstance(data, datetime):
                pii.append(data.strftime("%m-%d-%Y %H:%M:%S"))
            else:
                pii.append(data)
        message = ";".join(pii)
        print(message)


if __name__ == '__main__':
    main()
