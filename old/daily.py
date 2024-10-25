import requests, json, os

subscription_key = os.environ["newsapi"]
search_term = "election"
search_url = "https://api.bing.microsoft.com/v7.0/news"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

def req(cat):
    params  = {"cc": "US", "category": cat, "textDecorations": False, "textFormat": "HTML"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    # search_results = json.dumps(response.json())
    search_results = response.json()

    # print(search_results.type())
    print(search_results)
    descriptions = [article["name"].replace("&#39;", "") for article in search_results["value"]]
    links = [article["url"] for article in search_results["value"]]

    pairs = list(zip(descriptions, links))
    res = [{"desc":x[0], "url": x[1]} for x in pairs]

    with open(f'{cat.lower()}.json', 'w') as fp:
        json.dump(res, fp)

with open("cli/cats.txt", "r") as f:
    cats = f.read().split("\n")

    for x in cats[:1]:
        req(x)
    

    params  = {"cc": "US", "textDecorations": False, "textFormat": "HTML"}

    response = requests.get(search_url+"/trendingtopics", headers=headers, params=params)
    response.raise_for_status()
    # search_results = json.dumps(response.json())
    search_results = response.json()

    # print(search_results.type())
    print(search_results)
    descriptions = [article["query"]["text"].replace("&#39;", "") for article in search_results["value"]]
    links = [article["webSearchUrl"] for article in search_results["value"]]

    pairs = list(zip(descriptions, links))
    res = [{"desc":x[0], "url": x[1]} for x in pairs]

    with open('trending.json', 'w') as fp:
        json.dump(res, fp)
