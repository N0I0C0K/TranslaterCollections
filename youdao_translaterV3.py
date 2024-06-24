from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64
from requests import session
from utils import get_useragent
import time
import random
import json
from rich.pretty import pprint


class YoudaoTranslater:
    def __init__(self) -> None:
        self.sess = session()
        self.sess.proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "origin": "https://fanyi.youdao.com",
            "referer": "https://fanyi.youdao.com/",
        }
        # params = {
        #     "_npid": "fanyiweb",
        #     "_ncat": "pageview",
        #     "_ncoo": str(2147483647 * random.uniform(0, 1)),
        #     "_nssn": "NULL",
        #     "_nver": "1.2.0",
        #     "_ntms": self.__sticTime(),
        # }
        # self.sess.get("https://rlogs.youdao.com/rlog.php", params=params)
        self.sess.cookies.set(
            "OUTFOX_SEARCH_USER_ID_NCOO",
            f"{random.randint(100000000, 999999999)}.{random.randint(100000000, 999999999)}",
        )
        self.sess.cookies.set(
            "OUTFOX_SEARCH_USER_ID",
            f"{random.randint(100000000, 999999999)}@{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        )
        params = {
            "keyid": "webfanyi-key-getter",
        } | self.__base_body("asdjnjfenknafdfsdfsd")
        res = self.sess.get("https://dict.youdao.com/webtranslate/key", params=params)
        t = res.json()
        self.key = t["data"]["secretKey"]

    def get_lan_list(self) -> dict:
        res = self.sess.get(
            "https://api-overmind.youdao.com/openapi/get/luna/dict/luna-front/prod/langType"
        )
        return res.json()["data"]["value"]["textTranslate"]

    def __sticTime(self) -> str:
        return str(int(time.time() * 1000))

    def __sign(self, t: str, key: str) -> str:
        return (
            MD5.new(
                f"client=fanyideskweb&mysticTime={t}&product=webfanyi&key={key}".encode()
            )
            .digest()
            .hex()
        )

    def __base_body(self, key: str) -> dict:
        t = self.__sticTime()
        return {
            "sign": self.__sign(t, key),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": t,
            "keyfrom": "fanyi.web",
        }

    def __decode(self, src: str) -> dict:
        key = b"ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
        iv = b"ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
        cryptor = AES.new(
            MD5.new(key).digest()[:16], AES.MODE_CBC, MD5.new(iv).digest()[:16]
        )
        res = cryptor.decrypt(base64.urlsafe_b64decode(src))
        txt = res.decode("utf-8")
        return json.loads(txt[: txt.rindex("}") + 1])

    def translate(self, src: str, fromLan: str = "auto", toLan: str = "auto"):
        data = {
            "i": src,
            "from": fromLan,
            "to": toLan,
            "dictResult": True,
            "keyid": "webfanyi",
        } | self.__base_body(self.key)
        res = self.sess.post("https://dict.youdao.com/webtranslate", data=data)
        return self.__decode(res.text)


def main():
    translater = YoudaoTranslater()
    times = 0
    while True:
        pprint(translater.translate(input(">"), toLan="auto"))
        times += 1
    print(f"times: {times}")


if __name__ == "__main__":
    main()
