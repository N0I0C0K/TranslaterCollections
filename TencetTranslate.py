from requests import session
from utils import get_useragent
from rich.pretty import pprint
from translators.server import QQFanyi

a = QQFanyi()
pprint(a.qqFanyi_api('hello', is_detail_result=True))
pprint(a.language_map)



if __name__ == "__main__":
    pass
