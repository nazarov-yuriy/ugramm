from .base_engine import BaseEngine, CheckResult, Match


class DummyEngine(BaseEngine):
    @staticmethod
    def name() -> str:
        return "dummy"

    @staticmethod
    def version() -> str:
        return "dummy 0.1"

    def check(self, text: str) -> CheckResult:
        res = CheckResult(self.version())
        if "Don't need a consolidation agreement so we don't have to negotiate one." == text:
            res.matches.append(Match(
                36, 0, quickfix=","
            ))
        res.fill_fixed(text)
        return res
