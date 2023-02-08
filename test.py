from requests import post

while True:
    k = input(">")
    res = post("https://fanyi.baidu.com/sug", data={"kw": k})
    print(res.json())
