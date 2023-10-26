import logging
from sys import stdout

from termcolor import colored


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.DEBUG)  # Set global logging level to DEBUG

        ch = logging.StreamHandler(stdout)
        ch.setFormatter(ColorizedFormatter())
        self.addHandler(ch)


class ColorizedFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': 'light_grey',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))
