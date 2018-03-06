import logging
from functools import partial

import requests

from newsapi.newsapi_auth import NewsApiAuth


LOGGER = logging.getLogger()


class NewsApiClient(object):

    def __init__(self, api_key, api_url='https://newsapi.org/v2/', timeout=30):
        self._url = api_url.rstrip('/')
        self._get = partial(requests.get,
                            auth=NewsApiAuth(api_key=api_key),
                            timeout=timeout)

    def top_headlines(self, q=None, sources=None, language=None, country=None,
                      category=None, page_size=None, page=None):
        # Define Payload
        payload = {}
        payload['q'] = q
        payload['sources'] = ','.join(sources) if sources else None
        payload['language'] = language
        payload['country'] = country
        payload['category'] = category
        payload['pageSize'] = page_size
        payload['page'] = page

        # Send Request
        LOGGER.debug("Params %s", payload)
        return self._get(self._url + '/top-headlines', params=payload).json()

    def everything(self, q=None, sources=None, domains=None,
                   from_parameter=None, to=None, language=None,
                   sort_by=None, page=None, page_size=None):
        # Define Payload
        payload = {}
        payload['q'] = ','.join(q) if q else None
        payload['sources'] = ','.join(sources) if sources else None
        payload['domains'] = ','.join(domains) if domains else None
        payload['from'] = from_parameter
        payload['to'] = to
        payload['language'] = ','.join(language) if language else None
        payload['sortBy'] = sort_by
        payload['page'] = page
        payload['pageSize'] = page_size

        # Send Request
        LOGGER.debug("Params %s", payload)
        return self._get(self._url + '/everything', params=payload).json()

    def sources(self, category=None, language=None, country=None):
        # Define Payload
        payload = {}
        payload['category'] = category
        payload['language'] = language
        payload['country'] = country

        # Send Request
        LOGGER.debug("Params %s", payload)
        return self._get(self._url + '/sources', params=payload).json()
