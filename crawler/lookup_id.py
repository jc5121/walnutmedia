import requests
from bs4 import BeautifulSoup
from httplib import BadStatusLine


def get_fb_id(user_id):

    url = "http://lookup-id.com/"
    payload = "fburl=https%3A%2F%2Fwww.facebook.com%2F" + \
              user_id + "&check=Lookup&undefined="
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "en-US,en;q=0.9",
        'Cache-Control': "max-age=0",
        'Cookie': "__cfduid=d3c70cdcf80c02e93ff84184aa6edbca11544687257",
        'Referer': "http://lookup-id.com/",
        'Upgrade': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Postman-Token': "38d2b865-b000-4883-b342-42ef06b46b07"
        }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
    except BadStatusLine:
        print "Look up BadStatus."

    bs = BeautifulSoup(response.text, "lxml")
    code_span = bs.find('span', {'id': 'code'})
    if code_span is None:
        return 0
    code = code_span.text
    return code


if __name__ == '__main__':
    get_fb_id('josh.mitchem.1')