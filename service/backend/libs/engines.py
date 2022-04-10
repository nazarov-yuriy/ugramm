from abc import ABCMeta, abstractmethod
import language_tool_python


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


class EngineFactory:
    def __init__(self):
        self.engines = {
            engine.name(): engine for engine in [
                DummyEngine,
                LanguageToolEngine,
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
