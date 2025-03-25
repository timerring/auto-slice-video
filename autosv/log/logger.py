# Copyright (c) 2025 auto-slice-video

import logging
import time
import os
from typing import Optional
from functools import partial


class Logger:
    def __init__(self, log_file_prefix: Optional[str] = None):
        self.log_file_prefix = log_file_prefix
        self._logger = None

    def __get__(self, instance, owner):
        if self._logger is None:
            self._logger = self._create_logger()
        return self._logger

    def _create_logger(self):
        logger = logging.getLogger(f"{self.log_file_prefix}")
        if not logger.handlers:
            logger.setLevel("DEBUG")
            formatter = logging.Formatter(
                "[%(levelname)s] - [%(asctime)s %(name)s] - %(message)s"
            )

            # console output
            console_handler = logging.StreamHandler()
            console_handler.setLevel("INFO")
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger


class Log:
    def __init__(self, log_file_prefix: Optional[str] = None):
        self.logger = Logger(log_file_prefix)

    @property
    def debug(self):
        return partial(self.logger.__get__(None, None).debug)

    @property
    def info(self):
        return partial(self.logger.__get__(None, None).info)

    @property
    def warning(self):
        return partial(self.logger.__get__(None, None).warning)

    @property
    def error(self):
        return partial(self.logger.__get__(None, None).error)

    @property
    def critical(self):
        return partial(self.logger.__get__(None, None).critical)
