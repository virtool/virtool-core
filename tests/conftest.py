from .fixtures import *

pytest_plugins = [
    "tests.fixtures.__init__"
]



def pytest_addoption(parser):
    parser.addoption(
        "--db-connection-string",
        action="store",
        default="mongodb://localhost:27017"
    )

    parser.addoption(
        "--redis-connection-string",
        action="store",
        default="redis://localhost:6379"
    )
