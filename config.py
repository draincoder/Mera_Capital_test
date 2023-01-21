import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Deribit:
    client_id: str
    client_secret: str
    pause: int


@dataclass
class Config:
    db: DbConfig
    deribit: Deribit


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    deribit = config["deribit"]
    return Config(
        db=DbConfig(**config["db"]),
        deribit=Deribit(
            client_id=deribit.get("client_id"),
            client_secret=deribit.get("client_secret"),
            pause=deribit.getint("pause"),
        ),
    )
