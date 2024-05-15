#!/usr/bin/env python3
"""
Module that has many functions that deals with personal data.
"""


import logging
import re


def filter_datum(fields, redaction, message, separator):
    """ Obfuscate fields from a log string """
    for field in fields:
        regex = field + "=(.*?)" + separator
        match = re.search(regex, message)
        message = re.sub(match.group(1), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields,
                               RedactingFormatter.REDACTION,
                               record.msg,
                               RedactingFormatter.SEPARATOR)
        return super().format(record)
