import requests, json, redis, sys

proxies = {"xx": "ip:port", "zz": "ip:port"}

try:
    rdb = redis.ConnectionPool(connection_class=redis.UnixDomainSocketConnection, path="/var/run/redis/redis-server.sock")
    conn = redis.Redis(connection_pool=rdb)
    conn.ping() 
except redis.ConnectionError:
    raise SystemExit('Connecting to Redis server has failed')

def getFromAPI(proxies, data):
    try:
        r = requests.get("https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=AfLsg42", proxies=proxies, timeout=10)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        print("Request timeout")
        return
    except requests.exceptions.RequestException as e:
        print(proxies, e)
        return
    except requests.exceptions.HTTPError as e:
        print(proxies, e)
        return

    try:
        dist = json.loads(r.text)
    except ValueError:
        print('Decoding JSON has failed')
        return
        
    for val in dist: data.append({'username': val["username"], 'gender': val["gender"], 'current_show': val["current_show"], 'num_users': val["num_users"], 'num_followers': val["num_followers"], 'block_from_countries': val["block_from_countries"]})


data = []
for proxy in proxies:
    print("Start getFromAPI", proxies[proxy])
    getFromAPI({'http': "http://"+proxies[proxy], 'https': "http://"+proxies[proxy]}, data)

data.sort(key=lambda item: item["num_users"], reverse=True)

rooms = {}
for val in data:
    if val["username"] in rooms:
        continue
    rooms[val["username"]] = {'gender': val["gender"], 'current_show': val["current_show"], 'num_users': val["num_users"], 'num_followers': val["num_followers"], 'block_from_countries': val["block_from_countries"]}

print(len(rooms))

try:
    conn.set('chaturbateList', json.dumps(rooms), ex=86400)
except redis.ConnectionError:
    raise SystemExit('Writing JSON to Redis server has failed')
