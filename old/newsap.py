from newsapi import NewsApiClient
import json

# Init
newsap = NewsApiClient(api_key='a49510fe0fe641e49fc2c0ead5a8f171')

# /v2/top-headlines
top_headlines = newsap.get_top_headlines(
                                        category='general',
                                        q = 'harris trump',
                                        language='en',
                                        country = 'us'
                                    )

# /v2/everything
all_articles = newsap.get_everything(q='U.S. election',
                                      language='en',
                                    #   country = 'us',
                                      )

# /v2/top-headlines/sources
sources = newsap.get_sources()

with open('result.json', 'w') as fp:
    json.dump(top_headlines, fp)

# print(top_headlines.type())
# print(all_articles)
# print(sources)
