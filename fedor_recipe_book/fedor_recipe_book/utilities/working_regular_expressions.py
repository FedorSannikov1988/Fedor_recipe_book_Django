import re


class WorkingWithRegularExpressions:

    @staticmethod
    def checking_string(string: str, pattern: str) -> bool:
        return re.match(pattern, string) is not None
