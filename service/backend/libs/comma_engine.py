from abc import ABC
from datasets import load_metric
from functools import lru_cache
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, RobertaTokenizer
from typing import Union
from .base_engine import BaseEngine, CheckResult, Match


class CommaBase(BaseEngine, ABC):
    DEFAULT = "O"
    COMMA = "B-COMMA"

    def __init__(self):
        self.model_path = ""
        self.label_list = [self.DEFAULT, self.COMMA]

    @lru_cache
    def _get_model(self) -> AutoModelForTokenClassification:
        return AutoModelForTokenClassification.from_pretrained(
            self.model_path, num_labels=len(self.label_list)
        )

    @lru_cache
    def _get_tokenizer(self) -> Union[AutoTokenizer, RobertaTokenizer]:
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
        predictions = torch.argmax(predictions.logits.squeeze(), axis=-1)  # noqa
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

    @staticmethod
    def _pad(matrix):
        max_len = max(len(row) for row in matrix)
        for row in matrix:
            row.extend([0] * (max_len - len(row)))

    def evaluate(self, texts, batch_size=64) -> dict:
        tokenizer = self._get_tokenizer()
        model = self._get_model()
        metric = load_metric("seqeval")
        word_preds = []

        for offset in range(0, len(texts), batch_size):
            batch = texts[offset:offset + batch_size]
            words_without_comma = [[word.replace(",", "") for word in text.split(" ")] for text in batch]
            tokens = tokenizer(words_without_comma, truncation=True, is_split_into_words=True)
            self._pad(tokens["input_ids"])
            self._pad(tokens["attention_mask"])
            batch_pred = model.forward(
                input_ids=torch.tensor(tokens['input_ids']), attention_mask=torch.tensor(tokens['attention_mask']))
            batch_pred = torch.argmax(batch_pred.logits.squeeze(), axis=-1)  # noqa

            for i in range(len(batch)):
                word_ids = tokens.word_ids(batch_index=i)
                word_preds.append([self.label_list[0] for _ in words_without_comma[i]])
                for pred, word_id in zip(batch_pred[i].numpy(), word_ids):
                    if word_id is not None and pred != 0:
                        word_preds[-1][word_id] = self.label_list[pred]
        labels = [
            [self.COMMA if "," in token else self.DEFAULT for token in text.split(" ")]
            for text in texts
        ]
        return metric.compute(predictions=word_preds, references=labels)


class CommaDistilRoberta(CommaBase):
    def __init__(self):
        super().__init__()
        self.model_path = "./comma-distilroberta-base-3domains/"

    @staticmethod
    def name() -> str:
        return "comma_distil_roberta"

    @staticmethod
    def version() -> str:
        return "comma_distil_roberta 0.1"


class CommaRoberta(CommaBase):
    def __init__(self):
        super().__init__()
        self.model_path = "./comma-roberta-base-3domains-more-data/"

    @staticmethod
    def name() -> str:
        return "comma_roberta"

    @staticmethod
    def version() -> str:
        return "comma_roberta 0.1"
