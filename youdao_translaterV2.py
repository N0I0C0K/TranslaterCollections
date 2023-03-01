from requests import session
from utils import get_useragent
from rich.pretty import pprint
import random
import time


class YoudaoV2Translater:
    def __init__(self) -> None:
        self.sess = session()
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "origin": "https://ai.youdao.com",
            "referer": "https://ai.youdao.com/",
        }

    def translate(self, s: str):
        res = self.sess.post(
            "https://aidemo.youdao.com/trans",
            data={"q": s, "from": "Auto", "to": "Auto"},
        )
        return res.json()


if __name__ == "__main__":
    a = YoudaoV2Translater()
    times = 0
    while True:
        pprint(a.translate(input(">")))
        times += 1
