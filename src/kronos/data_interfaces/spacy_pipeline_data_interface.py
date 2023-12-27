from pathlib import Path
import spacy
from spacy.language import Language

from kronos.nodes.spacy_patterns import LIST_LOC


class SpacyPipelineDataInterface:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        
    def load(self) -> Language:
        nlp = spacy.load(self.filepath)
        patterns = [{"label": "LOC", "pattern": [{"LOWER": {"FUZZY": token.text}} for token in nlp(loc)]} for loc in LIST_LOC]
        ruler = nlp.add_pipe("entity_ruler")
        ruler.add_patterns(patterns)
        
        return nlp
