import requests
import bs4

r = requests.get('https://m.facebook.com/luckydayapp/')
print type(r)
print r.status_code
print r.encoding
print r.cookies
