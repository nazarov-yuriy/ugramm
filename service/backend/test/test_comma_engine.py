import unittest
import json
import wget
import os
from libs.comma_engine import CommaRoberta, CommaDistilRoberta
import tarfile

SKIP_SLOW = int(os.getenv("SKIP_SLOW", "0"))


@unittest.skipIf(SKIP_SLOW, "slow")
class TestCommaEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Download test data
        if not os.path.exists("test.txt"):
            wget.download("https://storage.yandexcloud.net/jbos/test.txt")

        # Download models if needed
        engine = CommaRoberta()
        if not os.path.exists(engine.model_path):
            filename = wget.download("https://storage.yandexcloud.net/jbos/comma-roberta-base-3domains-more-data.tar")
            with tarfile.open(filename) as tar:
                tar.extractall('.')

        engine = CommaDistilRoberta()
        if not os.path.exists(engine.model_path):
            filename = wget.download("https://storage.yandexcloud.net/jbos/comma-distilroberta-base-3domains.tar")
            with tarfile.open(filename) as tar:
                tar.extractall('.')

    def test_noop_roberta(self):
        engine = CommaRoberta()
        check_res = engine.check("We love contributions!")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "We love contributions!", "matches": [], "version": "comma_roberta 0.1"}'
        self.assertEqual(json_text, expected)

    def test_noop_distilroberta(self):
        engine = CommaDistilRoberta()
        check_res = engine.check("We love contributions!")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "We love contributions!", "matches": [], "version": "comma_distil_roberta 0.1"}'
        self.assertEqual(json_text, expected)

    def test_minimal_roberta(self):
        engine = CommaRoberta()
        check_res = engine.check("Currently only committers can assign issues to themselves "
                                 "so just add a comment if you're starting work on it.")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "Currently, only committers can assign issues to themselves, so just add a comment if ' \
                   'you\'re starting work on it.", "matches": [{"length": 0, "message": null, "quickfix": ",", ' \
                   '"rule": null, "start": 9}, {"length": 0, "message": null, "quickfix": ",", "rule": null, ' \
                   '"start": 57}], "version": "comma_roberta 0.1"}'
        self.assertEqual(json_text, expected)

    def test_minimal_distilroberta(self):
        engine = CommaDistilRoberta()
        check_res = engine.check("Currently only committers can assign issues to themselves "
                                 "so just add a comment if you're starting work on it.")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "Currently, only committers can assign issues to themselves, so just add a comment if ' \
                   'you\'re starting work on it.", "matches": [{"length": 0, "message": null, "quickfix": ",", ' \
                   '"rule": null, "start": 9}, {"length": 0, "message": null, "quickfix": ",", "rule": null, ' \
                   '"start": 57}], "version": "comma_distil_roberta 0.1"}'
        self.assertEqual(json_text, expected)

    def test_metrics_roberta(self):
        engine = CommaRoberta()
        with open("test.txt", "r") as f:
            texts = f.read().splitlines()
        res = engine.evaluate(texts[::100])
        print(res)
        self.assertTrue(res['overall_f1'] >= 0.84)
        self.assertTrue(res['overall_recall'] >= 0.84)
        self.assertTrue(res['overall_precision'] >= 0.85)

    def test_metrics_distilroberta(self):
        engine = CommaDistilRoberta()
        with open("test.txt", "r") as f:
            texts = f.read().splitlines()
        res = engine.evaluate(texts[::100])
        self.assertTrue(res['overall_f1'] >= 0.79)
        self.assertTrue(res['overall_recall'] >= 0.77)
        self.assertTrue(res['overall_precision'] >= 0.8)

    def test_large_text_roberta(self):
        engine = CommaRoberta()
        text = "Hello world.\n" * 4096
        engine.check(text)

    def test_large_text_distilroberta(self):
        engine = CommaDistilRoberta()
        text = "Hello world.\n" * 4096
        engine.check(text)
