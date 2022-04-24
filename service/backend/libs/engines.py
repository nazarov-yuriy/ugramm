from abc import ABCMeta, abstractmethod, ABC
import language_tool_python
import nemo.collections.nlp as nemo_nlp
from functools import lru_cache
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification


class Match:
    def __init__(self, start: int, length: int, rule: str = None, quickfix: str = None, message: str = None):
        self.start = start
        self.length = length
        self.rule = rule
        self.quickfix = quickfix
        self.message = message

    def serialize(self):
        return self.__dict__


class CheckResult:
    def __init__(self, version):
        self.version = version
        self.matches = []
        self.fixed = None

    def fill_fixed(self, text: str):
        res = []
        pos = 0
        for match in self.matches:
            if match.quickfix is None:
                continue
            assert pos <= match.start
            res.append(text[pos:match.start])
            res.append(match.quickfix)
            pos = match.start + match.length
        res.append(text[pos:])
        self.fixed = "".join(res)

    def serialize(self):
        res = self.__dict__
        res["matches"] = [x.serialize() for x in res["matches"]]
        return res


class BaseEngine(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def version() -> str:
        pass

    @abstractmethod
    def check(self, text: str) -> CheckResult:
        pass


class DummyEngine(BaseEngine):
    @staticmethod
    def name():
        return "dummy"

    @staticmethod
    def version():
        return "dummy 0.1"

    def check(self, text: str) -> CheckResult:
        res = CheckResult(self.version())
        if "Don't need a consolidation agreement so we don't have to negotiate one." == text:
            res.matches.append(Match(
                36, 0, quickfix=","
            ))
        res.fill_fixed(text)
        return res


class LanguageToolEngine(BaseEngine):
    def __init__(self):
        self.lt = language_tool_python.LanguageTool('en-US', remote_server='http://lt:8081')  # ToDo: make configurable

    @staticmethod
    def name():
        return "languagetool"

    @staticmethod
    def version():
        return "languagetool 5.7.0"

    def check(self, text: str) -> CheckResult:
        res = CheckResult(self.version())
        for match in self.lt.check(text):
            if match.ruleId == "COMMA_COMPOUND_SENTENCE" and match.replacements and match.replacements[0][0] == ",":
                res.matches.append(Match(
                    match.offset, 0, quickfix=","
                ))
        res.fill_fixed(text)
        return res


class NemoBase(BaseEngine, ABC):
    def __init__(self):
        self.model_name = ""

    @lru_cache
    def _get_model(self):
        return nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name=self.model_name)

    @staticmethod
    def _clean_punctuation(text):
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
    def name():
        return "nemo_punctuation_en_distilbert"

    @staticmethod
    def version():
        return "nemo_punctuation_en_distilbert 1.8.1"


class NemoBert(NemoBase):
    def __init__(self):
        super().__init__()
        self.model_name = "punctuation_en_bert"

    @staticmethod
    def name():
        return "nemo_punctuation_en_bert"

    @staticmethod
    def version():
        return "nemo_punctuation_en_bert 1.8.1"


class CommaBase(BaseEngine, ABC):
    DEFAULT = "O"
    COMMA = "B-COMMA"

    def __init__(self):
        self.model_path = ""
        self.label_list = [self.DEFAULT, self.COMMA]

    @lru_cache
    def _get_model(self):
        return AutoModelForTokenClassification.from_pretrained(
            self.model_path, num_labels=len(self.label_list)
        )

    @lru_cache
    def _get_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_path)

    def check(self, text: str) -> CheckResult:
        tokenizer = self._get_tokenizer()
        model = self._get_model()
        words = text.split(" ")
        words_without_comma = [word.replace(",", "") for word in words]
        tokens = tokenizer(words_without_comma, truncation=True, is_split_into_words=True)
        word_ids = tokens.word_ids()
        predictions = model.forward(
            input_ids=torch.tensor(tokens['input_ids']).unsqueeze(0),
            attention_mask=torch.tensor(tokens['attention_mask']).unsqueeze(0)
        )
        predictions = torch.argmax(predictions.logits.squeeze(), axis=-1)
        word_preds = [self.label_list[0] for _ in words]
        for pred, word_id in zip(predictions.numpy(), word_ids):
            if word_id is not None and pred != 0:
                word_preds[word_id] = self.label_list[pred]
        offsets = []
        offset = 0
        for word_id, word in enumerate(words):
            offsets.append(offset)
            offset += 1 + len(word)

        res = CheckResult(self.version())
        for word_id, prediction in enumerate(word_preds):
            word = words[word_id]
            if self.COMMA == prediction and "," not in word:
                res.matches.append(Match(
                    offsets[word_id] + len(word), 0, quickfix=","
                ))
        res.fill_fixed(text)
        return res


class CommaDistilRoberta(CommaBase):
    def __init__(self):
        super().__init__()
        self.model_path = "./comma-distilroberta-base-3domains/"

    @staticmethod
    def name():
        return "comma_distil_roberta"

    @staticmethod
    def version():
        return "comma_distil_roberta 0.1"


class CommaRoberta(CommaBase):
    def __init__(self):
        super().__init__()
        self.model_path = "./comma-roberta-base-3domains-more-data/"

    @staticmethod
    def name():
        return "comma_roberta"

    @staticmethod
    def version():
        return "comma_roberta 0.1"


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
