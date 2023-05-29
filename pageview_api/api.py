# API docs: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews
# API call structure: https://wikimedia.org/api/rest_v1/metrics/pageviews/{endpoint}/{parameter 1}/{parameter 2}/.../{parameter N}
from typing import Literal
import requests
from datetime import datetime

WProject = Literal['en.wikipedia', 'no.wikipedia.org', 'all-projects']
WAccess = Literal['all-access', 'mobile-app', 'desktop']
WCountry = Literal['JP', 'US', 'NO']
WAgent = Literal['all-agents', 'spider', 'user', 'automated']
WGrain = Literal['hourly', 'daily', 'monthly']

class PageviewAPI:
    ROOT_URL = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/'
    
    def __init__(self, user_agent:str, session:requests.Session=None) -> None:
        self._session = session if session else requests.Session()
        self.user_agent = user_agent

    def per_article(self, project:WProject, access:WAccess, agent:WAgent, article:str, grain:WGrain, start:datetime, end: datetime) -> requests.Response:
        path = f'per-article/{project}/{access}/{agent}/{article}/{grain}/{int(start.timestamp())}/{int(end.timestamp())}'
        return self._request(path)
    
    def top(self, project:WProject, access:WAccess, year:str, month:str, day:str = 'all-days') -> requests.Response:
        path = f'top/{project}/{access}/{year}/{month:0>2}/{day:0>2}'
        return self._request(path)

    def top_countries(self, project:WProject, access:WAccess, year:str, month:str) -> requests.Response:
        path = f'top-by-country/{project}/{access}/{year}/{month:0>2}'
        return self._request(path)
    
    def top_per_country(self, cc:WCountry, access:WAccess, year:str, month:str, day:str='all-days') -> requests.Response:
        path = f'top-per-country/{cc}/{access}/{year}/{month:0>2}/{day:0>2}'
        return self._request(path)

    def aggregate(self, project:WProject, access:WAccess, agent:WAgent, grain:WGrain, start:datetime, end:datetime) -> requests.Response:
        path = f'aggregate/{project}/{access}/{agent}/{grain}/{int(start.timestamp())}/{int(end.timestamp())}'
        return self._request(path)
    
    def _request(self, path) -> requests.Response:
        return self._session.get(self.ROOT_URL + path, headers={'User-Agent':self.user_agent})