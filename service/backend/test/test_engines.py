import unittest
from libs.base_engine import BaseEngine
from libs.engines import EngineFactory


class TestEngineFactory(unittest.TestCase):
    def test_list(self):
        factory = EngineFactory()
        expected = [
            "dummy",
            "languagetool",
            "nemo_punctuation_en_distilbert",
            "nemo_punctuation_en_bert",
            "comma_distil_roberta",
            "comma_roberta"
        ]
        self.assertEqual(factory.get_list(), expected)

    def test_get(self):
        factory = EngineFactory()
        engine_name = "dummy"
        engine = factory.get_engine(engine_name)
        self.assertIsInstance(engine, BaseEngine)
        self.assertEqual(engine.name(), engine_name)
