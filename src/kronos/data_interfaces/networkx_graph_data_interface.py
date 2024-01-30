from pathlib import Path
import logging

from networkx import Graph, node_link_data, node_link_graph
import orjson

logger = logging.getLogger(__name__)

class NetworkXGraphDataInterface:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
    
    def save(self, nx_g: Graph) -> None:
        with open(self.filepath, "wb") as f:
            data = node_link_data(nx_g)

            f.write(orjson.dumps(data))

            logger.info(f"Saved a type {type(nx_g)} object to {self.filepath}")
    
    def load(self) -> Graph:
        with open(self.filepath, "rb") as f:
            nx_g = node_link_graph(data=orjson.loads(f.read()))

            logger.info(f"Loaded a {type(nx_g)} object from {self.filepath}")

            return nx_g
