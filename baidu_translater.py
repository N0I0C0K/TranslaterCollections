from requests import session
from utils import get_useragent
from subprocess import Popen, PIPE
from rich.pretty import pprint
import re


class BadiDuTranslater:
    def __init__(self) -> None:
        self.sess = session()
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "Host": "fanyi.baidu.com",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Connection": "keep-alive",
        }
        self.sess.get("https://fanyi.baidu.com")
        res = self.sess.get("https://fanyi.baidu.com").content.decode()
        self.token = re.findall(r"token: '(.*)',", res, re.M)[0]

    def lan_detect(self, src: str) -> str:
        fromLan = self.sess.post(
            "https://fanyi.baidu.com/langdetect", data={"query": src}
        ).json()["lan"]
        return fromLan

    def translate(self, source: str, toLan: str = "", fromLan: str = "") -> str:
        if fromLan == "":
            fromLan = self.sess.post(
                "https://fanyi.baidu.com/langdetect", data={"query": source}
            ).json()["lan"]
        if toLan == "":
            toLan = "zh" if fromLan != "zh" else "en"
        node = Popen(["node", "./sign.js", source], stdout=PIPE)
        node.wait()
        sign = node.stdout.readline().decode()
        # 这里多次尝试是因为请求不会100%成功，多次请求直到成功
        tryTimes = 0
        try:
            while tryTimes < 100:
                res = self.sess.post(
                    "https://fanyi.baidu.com/v2transapi",
                    params={"from": fromLan, "to": toLan},
                    data={
                        "from": fromLan,
                        "to": toLan,
                        "query": source,
                        "simple_means_flag": "3",
                        "transtype": "realtime",
                        "sign": sign,
                        "token": self.token,
                        "domain": "common",
                    },
                )
                if "trans_result" in res.text:
                    break
                tryTimes += 1
            else:
                print("err in get")
                return
        except:
            print("err")
            pass
        data = res.json()
        pprint(data)


def main():
    # res = post("https://fanyi.baidu.com/langdetect", data={"query": "你好"}).json()["lan"]
    # print(res)

    baidu = BadiDuTranslater()
    while True:
        soc = input()

        baidu.translate(soc)


if __name__ == "__main__":
    main()
