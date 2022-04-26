from abc import ABC
from functools import lru_cache
import logging

logging.disable(logging.CRITICAL)  # to mute nemo
from nemo.collections.nlp.models import PunctuationCapitalizationModel  # noqa

logging.disable(logging.NOTSET)
from .base_engine import BaseEngine, CheckResult, Match  # noqa


class NemoBase(BaseEngine, ABC):
    def __init__(self):
        self.model_name = ""

    @lru_cache
    def _get_model(self) -> PunctuationCapitalizationModel:
        return PunctuationCapitalizationModel.from_pretrained(model_name=self.model_name)

    @staticmethod
    def _clean_punctuation(text) -> str:
        return text.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

    def check(self, text: str) -> CheckResult:
        res = CheckResult(self.version())
        # nemo expects text without punctuation
        clean_text = self._clean_punctuation(text)
        predictions = self._get_model().add_punctuation_capitalization([clean_text], return_labels=True)[0].split(" ")
        word_ids = []
        words = []
        offsets = []
        offset = 0
        for word_id, word in enumerate(text.split(" ")):
            offsets.append(offset)
            words.append(word)
            offset += 1 + len(word)
            if self._clean_punctuation(word) != "":
                word_ids.append(word_id)

        for word_id, prediction in zip(word_ids, predictions):
            word = words[word_id]
            if "," in prediction and "," not in word:
                res.matches.append(Match(
                    offsets[word_id] + len(word), 0, quickfix=","
                ))
        res.fill_fixed(text)
        return res


class NemoDistilBert(NemoBase):
    def __init__(self):
        super().__init__()
        self.model_name = "punctuation_en_distilbert"

    @staticmethod
    def name() -> str:
        return "nemo_punctuation_en_distilbert"

    @staticmethod
    def version() -> str:
        return "nemo_punctuation_en_distilbert 1.8.1"


class NemoBert(NemoBase):
    def __init__(self):
        super().__init__()
        self.model_name = "punctuation_en_bert"

    @staticmethod
    def name() -> str:
        return "nemo_punctuation_en_bert"

    @staticmethod
    def version() -> str:
        return "nemo_punctuation_en_bert 1.8.1"
