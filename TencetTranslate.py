from requests import session
from utils import get_useragent


class TencetTranslater:
    def __init__(self) -> None:
        self.sess = session()
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "Origin": "https://fanyi.qq.com",
            "Referer": "https://fanyi.qq.com/",
        }
        self.sess.post("https://otheve.beacon.qq.com/analytics/upload?tp=js", data={})


if __name__ == "__main__":
    pass
