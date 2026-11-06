import logging
from configparser import ConfigParser
from enum import IntEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    filename=Path.cwd() / "log.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

_log_levels = {
    "0": "STATUS",
    "1": logging.DEBUG,
    "2": logging.INFO,
    "3": logging.WARNING,
    "4": logging.ERROR,
    "5": logging.CRITICAL,
}


class Log_Level(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def read_config_file(file_name: str) -> ConfigParser:
    cfg_file_folder = Path(Path.cwd().root) / "sparc4" / "config"
    cfg_file = cfg_file_folder / file_name
    if not cfg_file.exists():
        raise RuntimeError(f"file {cfg_file} not found")
    config = ConfigParser()
    config.read(cfg_file)

    return config


class S4ACS_Config(BaseModel):
    channel: int
    acs_mode: int
    image_path: Path
    log_file_path: Path
    log_level: Log_Level

    def to_sparc4_format(self) -> dict[str, Any]:
        new_dict = {key.replace("_", " "): val for key, val in self.model_dump().items()}
        new_dict["log level"] //= 10
        return new_dict

    @classmethod
    def from_config_file(cls, file_name: str) -> S4ACS_Config:
        parser = read_config_file(file_name)
        section_name = "channel configuration"
        return S4ACS_Config(
            channel=int(parser.get(section_name, "channel")),
            acs_mode=int(parser.get(section_name, "ACS mode")) == 1,
            image_path=Path(parser.get(section_name, "image path")),
            log_file_path=Path(parser.get(section_name, "log file path")),
            log_level=Log_Level(_log_levels[parser.get(section_name, "log level")]),
        )
