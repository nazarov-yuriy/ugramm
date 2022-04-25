from abc import abstractmethod, ABC


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


class BaseEngine(ABC):
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
