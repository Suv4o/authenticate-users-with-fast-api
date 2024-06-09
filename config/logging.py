import logging

logging.basicConfig(level=logging.INFO)


class Logger:
    def __init__(self, name):
        self.name = name

    def get(self):
        return logging.getLogger(self.name)
