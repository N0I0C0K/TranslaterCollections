import time
import random
import hashlib
from rich.pretty import pprint
from requests import session
from utils import get_useragent


def md5_encrype(src: str) -> str:
    md5 = hashlib.md5()
    md5.update(src.encode())
    return md5.hexdigest()


class YoudaoTranslater:
    def __init__(self) -> None:
        self.sess = session()
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "Origin": "https://fanyi.youdao.com",
            "Referer": "https://fanyi.youdao.com/",
        }
        params = {
            "_npid": "fanyiweb",
            "_ncat": "event",
            "_ncoo": str(2147483647 * random.uniform(0, 1)),
            "nssn": "NULL",
            "_nver": "1.2.0",
            "_ntms": str(int(time.time() * 1000)),
            "_nhrf": "newweb_translate_text",
        }
        self.sess.get("https://rlogs.youdao.com/rlog.php", params=params)

    def translate(self, src: str, fromLan: str = "AUTO", toLan: str = "AUTO") -> dict:
        ts = int(time.time() * 1000)
        salt = str(ts) + str(random.randint(0, 9))
        bv = md5_encrype(self.sess.headers.get("User-Agent"))
        sign = md5_encrype(f"fanyideskweb{src}{salt}Ygy_4c=r#e#4EX^NUGUc5")
        data = {
            "i": src,
            "from": fromLan,
            "to": toLan,
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        res = self.sess.post(
            "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",
            data=data,
        )
        return res.json()


def test():
    translater = YoudaoTranslater()
    times = 0
    while True:
        pprint(translater.translate(input(">")))
        times += 1
        print(times)


if __name__ == "__main__":
    test()
