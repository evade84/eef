import configparser

import typer

from eef import output


class Config:
    path: str

    def __init__(self):
        self.path = typer.get_app_dir("eef") + "/config"
        self._parser = configparser.ConfigParser()

    def read_node_url(self):
        files = self._parser.read(self.path)
        if not files:
            output.error(f"eef config does not exist ({self.path}).", terminate=True)
        try:
            node_url = self._parser["node"].get("url")
            if not node_url:
                raise KeyError()
            return node_url
        except KeyError:
            output.error("invalid eef config format.", terminate=True)


config = Config()
