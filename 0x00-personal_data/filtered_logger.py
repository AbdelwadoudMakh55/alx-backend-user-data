#!/usr/bin/env python3
""" doc doc doc """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate fields from a log string """
    for field in fields:
        match = re.search(rf'{field}=(.*?){separator}', message)
        if match:
            message = re.sub(match.group(1), redaction, message, 1)
    return message


class RedactingFormatter(logging.Formatter):
    """doc doc doc"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """doc doc doc"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """doc doc doc"""
        org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, org, self.SEPARATOR)
