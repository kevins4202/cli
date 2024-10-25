import requests, json, time, os

subscription_key = os.environ.get("newsapi_key")
path = os.environ.get("path")
search_term = "election"
search_url = "https://api.bing.microsoft.com/v7.0/news"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

topics = []

def run():
    with open(f'{path}/cats.txt', 'r') as fp:
        topics = fp.readlines()
        for i in range(len(topics)):
            topics[i] = topics[i].strip()
        print(topics)

    json_obj = {}
    with open(f'{path}/results/result.json', 'w') as fp:
        for topic in topics:
            # wait 3 seconds
            time.sleep(3)

            params  = {"cc": "US", "category": topic, "textDecorations": False, "textFormat": "HTML"}

            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            # search_results = json.dumps(response.json())
            search_results = response.json()

            # print(search_results.type())
            # print(search_results)
            descriptions = [article["name"] for article in search_results["value"]]
            urls = [article["url"] for article in search_results["value"]]

            print("\n\nSearch term: ", topic)

            for s in descriptions:
                print(s)

            res = {}

            for i in range(len(descriptions)):
                res[topic] = [{"description": descriptions[i], "url": urls[i]} for i in range(len(descriptions))]
            json_obj['date'] = time.strftime("%Y-%m-%d")
            json_obj['results'] = res
        
        json.dump(json_obj, fp)
        return json_obj
