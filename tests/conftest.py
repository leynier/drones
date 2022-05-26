from argparse import Namespace

from pytest import Config, Parser

option: Namespace | None = None


def pytest_addoption(parser: Parser):
    parser.addoption("--mode", action="store", default="mock")


def pytest_configure(config: Config):
    global option
    option = config.option
