from pydantic import BaseSettings


class Configs(BaseSettings):
    api_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs() -> Configs:
    return Configs()
