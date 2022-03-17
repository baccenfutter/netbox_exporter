import logging
import requests


class FetcherException(Exception):
    pass


class Fetcher(object):
    """Convenience class for fetching data from Netbox."""
    
    LIMIT = 1000
    BLACKLISTED_ENDPOINTS = ['status']

    def __init__(self, url: str, apikey: str) -> object:
        """
        :param url:     the URL to Netbox
        :param apikey:  the API auth-token
        """
        if not url.endswith('/api') and not url.endswith('/api/'):
            url = f"{url}/api/"
        self.url = url
        self.apikey = apikey

    @property
    def headers(self):
        """Helper property for obtaining the preformatted request headers."""
        return {
                "Authorization": f"Token {self.apikey}",
                "Content-Type": "application/json",
        }

    def fetch_index(self, url: str = None) -> dict:
        """Fetch an index from Netbox.

        Ignores all top-level sections listed in self.BLACKLISTED_ENDPOINTS.
        
        :param url: the URL of the index to fetch
        :return:    {section: url, ...}
        """
        if url is None:
            url = self.url
        logging.info(f"Fetching index: {url}")
        req = requests.get(
            url,
            headers=self.headers,
        )
        rc = req.status_code
        if rc != requests.status_codes.codes['OK']:
            raise FetcherException(f"Returned: {rc}")
        return {
            k: v for k, v in req.json().items()
            if k not in self.BLACKLISTED_ENDPOINTS
        }

    def fetch_data(self, url: str) -> list:
        """Fetch data from Netbox.
        
        Will loop through pagination until all data is retrieved.

        :param url: URL to fetch the data from
        :return: [item, ...]
        """
        data = []
        url = f"{url}?limit={self.LIMIT}"
        while url:
            logging.debug(f"Fetching: {url}")
            req = requests.get(
                url,
                headers=self.headers,
            )
            rc = req.status_code
            if rc != requests.status_codes.codes['OK']:
                if rc != 400:
                    raise FetcherException(f"Returned: {rc}")
            res = req.json()
            if 'results' in res:
                data.extend(res['results'])
            url = None
            if 'next' in res:
                if res['next'] != url:
                    url = res['next']
        return data
