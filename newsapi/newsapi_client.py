import logging
from functools import partial

import requests

from newsapi.newsapi_auth import NewsApiAuth


LOGGER = logging.getLogger()


class NewsApiClient(object):
    """Client for NewsApi.org, an API Key is required, get one at newsapi.org.
    """
    def __init__(self, api_key: str, api_url='https://newsapi.org/v2/',
                 timeout=30) -> None:
        self._url = api_url.rstrip('/')
        self._get = partial(requests.get,
                            auth=NewsApiAuth(api_key=api_key),
                            timeout=timeout)

    def top_headlines(self, q: list=None, sources: list=None,
                      language: str=None, country: str=None,
                      category: str=None, page_size: int=None, page: int=None):
        """Returns live top and breaking headlines for a country, specific
        category in a country, single source, or multiple sources..
        Optional parameters:
        q - return headlines w/ specified keywords.
        sources - return headlines of news sources! some Valid values are:
                  'bbc-news', 'fox-news', for more use NewsApiClient.sources()
        language - 2-letter ISO-639-1 code of the language you want to get
                   headlines for. Valid values are:
                   'ar','de','en','es','fr','he','it','nl','no','pt','ru','se',
                   'ud','zh'
        country: The 2-letter ISO 3166-1 code of the country you want
                       to get headlines for.
                       Valid values are:
                       'ae','ar','at','au','be','bg','br','ca','ch','cn','co',
                       'cu','cz','de','eg','fr','gb','gr','hk','hu','id','ie',
                       'il','in','it','jp','kr','lt','lv','ma','mx','my','ng',
                       'nl','no','nz','ph','pl','pt','ro','rs','ru','sa','se',
                       'sg','si','sk','th','tr','tw','ua','us'
        category - The category you want to get headlines for. Valid values:
                        'business','entertainment','general','health','science'
                        ,'sports','technology'
        page_size - The number of results to return per page (request).
                    20 is the default, 100 is the maximum.
        page - Use this to page through the results if the total results found
               is greater than the page size.
        """
        # Define Payload
        payload = {}
        payload['q'] = ','.join(q) if sources else None
        payload['sources'] = ','.join(sources) if sources else None
        payload['language'] = language
        payload['country'] = country
        payload['category'] = category
        payload['pageSize'] = page_size
        payload['page'] = page

        # Send Request
        LOGGER.debug("Params %s", payload)
        return self._get(self._url + '/top-headlines', params=payload).json()

    def everything(self, q: list=None, sources: list=None, domains: list=None,
                   from_parameter: str=None, to: str=None, language: str=None,
                   sort_by: str=None, page: int=None,
                   page_size: int=None) -> str:
        """Returns the subset of news publishers that top headlines...
        Optional parameters:

        language - The 2-letter ISO-639-1 code of the language you want
        to get headlines for.
        Valid values:
        'ar','de','en','es','fr','he','it','nl','no','pt','ru','se','ud','zh'

        country - The 2-letter ISO 3166-1 code of the country you want to get
        headlines from.
        Valid values:
        'ae','ar','at','au','be','bg','br','ca','ch','cn','co','cu','cz','de',
        'eg','fr','gb','gr','hk','hu','id','ie','il','in','it','jp','kr','lt',
        'lv','ma','mx','my','ng','nl','no','nz','ph','pl','pt','ro','rs','ru',
        'sa','se','sg','si','sk','th','tr','tw','ua','us'

        category - The category you want to get headlines for!
        Valid values:
        'business','entertainment','general','health','science','sports',
        'technology'
        """

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

    def sources(self, category: str=None, language: str=None,
                country: str=None) -> str:
        """Retrieve list of source names optionally filtering by category and
        language.
        """
        # Define Payload
        payload = {}
        payload['category'] = category
        payload['language'] = language
        payload['country'] = country

        # Send Request
        LOGGER.debug("Params %s", payload)
        return self._get(self._url + '/sources', params=payload).json()
