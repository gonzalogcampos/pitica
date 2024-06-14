import os as _os
import shutil as _shutil
import logging as _logging

from pitica import constants as _constants
from pitica.config_reader import ConfigReader as _ConfigReader
from pitica.generator.generator import Generator as _Generator

_logger = _logging.getLogger(__name__)


def generate_sources(directory: str, clean: bool):
    _logger.debug("Generating sources")

    config_filepath = _os.path.join(directory, _constants.SCHEMA_FILENAME)
    if not _os.path.exists(config_filepath):
        msg = f"Configuration file {config_filepath} not found."
        _logger.error(msg)
        raise FileNotFoundError(msg)

    if len(_os.listdir(directory)) != 1 and not clean:
        msg = f"Directory {directory} is not empty."
        _logger.error(msg)
        raise FileExistsError(msg)

    _logger.debug(f"Config filepath: {config_filepath}")
    _logger.debug(f"Output sources: {directory}")

    if clean:
        all_items = _os.listdir(directory)

        if _constants.SCHEMA_FILENAME not in all_items:
            msg = f"Directory {directory} is not a {_constants.NAME} dir."
            _logger.error(msg)
            raise FileNotFoundError(msg)

        _logger.debug("Cleaning output directory")

        for item in _os.listdir(directory):
            if item == _constants.SCHEMA_FILENAME:
                continue
            item_path = _os.path.join(directory, item)
            if _os.path.isdir(item_path):
                _shutil.rmtree(item_path)
            else:
                _os.remove(item_path)

    config = _ConfigReader(config_filepath).get_config()
    generator = _Generator(config)
    generator.generate(directory)
