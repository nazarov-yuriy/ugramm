import language_tool_python
from .base_engine import BaseEngine, CheckResult, Match


class LanguageToolEngine(BaseEngine):
    def __init__(self):
        self.lt = language_tool_python.LanguageTool('en-US', remote_server='http://lt:8081')  # ToDo: make configurable

    @staticmethod
    def name() -> str:
        return "languagetool"

    @staticmethod
    def version() -> str:
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
