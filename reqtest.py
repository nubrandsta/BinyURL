import requests


try:
    r = requests.get('http://www.qequeuqweuqweyuwewq.com',timeout=2.0)
    print(r.url)
except:
    print("Timedout?")
finally:
    print("done")