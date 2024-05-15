#!/usr/bin/env python3
"""
Module that has many functions that deals with personal data.
"""


import logging
import re
from typing import List


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


PII_FIELDS = ("name", "email", "phone", "password", "ip")


def get_logger() -> logging.Logger:
    """ Function that creates a logger """
    formatter = RedactingFormatter([])
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data = logging.getLogger("user_data",
                                  level=logging.INFO,
                                  propagate=False,
                                  handlers=[stream_handler])
    return user_data
