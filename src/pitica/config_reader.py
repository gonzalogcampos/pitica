import logging as _logging
import yaml as _yaml

_logger = _logging.getLogger(__name__)


class ConfigReader:
    def __init__(self, path):
        self._config = self._load(path)

    def _load(self, path):
        _logger.debug(f"Loading configuration file {path}")
        with open(path, "r") as file:
            config = _yaml.safe_load(file)
        return config

    def get_config(self):
        return self._config
