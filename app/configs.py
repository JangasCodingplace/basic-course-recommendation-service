import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class _Neo4j:
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    host = os.getenv("NEO4J_HOST")
    port = os.getenv("NEO4J_PORT")


BASE_DIR = Path(__file__).parent
NEO4J = _Neo4j()
EXEC_INITIAL_LOAD = os.getenv("EXEC_INITIAL_LOAD", "false").lower() == "true"
