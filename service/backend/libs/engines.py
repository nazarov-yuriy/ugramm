from .base_engine import BaseEngine
from .comma_engine import CommaDistilRoberta, CommaRoberta
from .dummy_engine import DummyEngine
from .language_tool_engine import LanguageToolEngine
from .nemo_engine import NemoDistilBert, NemoBert


class EngineFactory:
    def __init__(self):
        self.engines = {
            engine.name(): engine for engine in [
                DummyEngine,
                LanguageToolEngine,
                NemoDistilBert,
                NemoBert,
                CommaDistilRoberta,
                CommaRoberta,
            ]
        }
        self.cache = {}

    def get_engine(self, name: str) -> BaseEngine:
        if name not in self.cache:
            if name in self.engines:
                self.cache[name] = self.engines[name]()
            else:
                ...
        return self.cache[name]
