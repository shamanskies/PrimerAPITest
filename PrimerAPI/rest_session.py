from datetime import datetime
import json
import platform
import random
import sys
import time
import urllib.parse
import requests

from PrimerAPI.exceptions import *
from PrimerAPI.__init__ import __version__
from PrimerAPI.config import *

# Main module interface
class RestSession(object):
    def __init__(
        self,
        logger,
        JWT,
        base_url=DEFAULT_BASE_URL,
        retry_429_rate_limit=RETRY_429_RATE_LIMIT,
        retry_429_wait_time=RETRY_429_WAIT_TIME,
        retry_400_error=RETRY_400_ERROR,
        retry_400_error_wait_time=RETRY_400_ERROR_WAIT_TIME,
        maximum_retries=MAX_RETRIES,
        simulate=SIMULATE_API_CALLS,
    ):
        super(RestSession, self).__init__()

        # Initialize attributes and properties
        self._version = __version__
        self._jwt = str(JWT)
        self._base_url = str(base_url)
        self._retry_429_rate_limit = retry_429_rate_limit
        self._retry_429_wait_time = retry_429_wait_time
        self._retry_400_error = retry_400_error
        self._retry_400_error_wait_time = retry_400_error_wait_time
        self._max_retries = maximum_retries
        self._simulate = simulate

        # Initialize a new `requests` session
        self._req_session = requests.session()
        self._req_session.encoding = 'utf-8'

        # Check base URL & remove backslash
        if self._base_url[-1] == '/':
            self._base_url = self._base_url[:-1]

        # Update the headers for the session
        self._req_session.headers = {
            'Authorization': 'JWT ' + self._jwt,
            'Content-Type': 'application/json',
            "Accept": "application/json"
        }

        # Log API calls
        self._logger = logger
        self._parameters = {'version': self._version}
        self._parameters.update(locals())
        self._parameters.pop('self')
        self._parameters.pop('logger')
        self._parameters.pop('__class__')
        self._parameters['jwt'] = ''.join(['*' for i in range(len(self._jwt)-4)]) + self._jwt[-4:]
        if self._logger:
            self._logger.info(f'Primer API session initialized with these parameters: {self._parameters}')

    def request(self, metadata, method, url, **kwargs):
        # Metadata on endpoint
        tag = metadata['tags'][0]
        operation = metadata['operation']


        # # Update request kwargs with session defaults
        # if self._certificate_path:
        #     kwargs.setdefault('verify', self._certificate_path)
        # if self._requests_proxy:
        #     kwargs.setdefault('proxies', {'https': self._requests_proxy})
        # kwargs.setdefault('timeout', self._single_request_timeout)

        # Ensure proper base URL
        abs_url = self._base_url + url

        if 'app' in metadata:
            abs_url = abs_url.replace('/api', '')

        
        if 'api/v1/summary/' in url and method == 'GET':
            retries = 100 #max retries for RAG-V
        else:
            retries = self._max_retries # Set maximum number of retries

        if self._logger:
            self._logger.debug(metadata)
        if self._simulate and method != 'GET': # Option to override POST/PUT/DELETE calls
            if self._logger:
                self._logger.info(f'{tag}, {operation} - SIMULATED')
            return None
        else:
            response = None
            while retries > 0:
                # Make the HTTP request to the API endpoint
                try:
                    if response:
                        response.close()
                    if self._logger:
                        self._logger.info(f'{method} {abs_url} {", ".join(f"{key}={value}" for key, value in kwargs.items())}')
                    response = self._req_session.request(method, abs_url, allow_redirects=False, **kwargs)
                    reason = response.reason if response.reason else ''
                    status = response.status_code
                except requests.exceptions.RequestException as e:
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                    time.sleep(1)
                    retries -= 1
                    if retries == 0:
                        if e.response and e.response.status_code:
                            raise APIError(metadata, APIResponseError(e.__class__.__name__, e.response.status_code, str(e)))
                        else:
                            raise APIError(metadata, APIResponseError(e.__class__.__name__, 503, str(e)))
                    else:
                        continue

                # Handle 300 redirects automatically
                if str(status)[0] == '3':
                    pass
                elif status == 202 and method == 'GET':
                    retries -= 1 #this will occur w/ RAG-V summaries as this is how we implemented polling, will retry up to 10x times
                    self._logger.info(f'{status}, {response.json()}')
                    time.sleep(10)
                elif response.ok or (status == 202 and method == 'POST'): # 200 success
                    if 'data' in metadata:                                #ACCEPTED responsible is valid condition for POST method
                        if self._logger:
                            self._logger.info(f'{tag}, {operation} - {status} {reason}')
                        return response
                    else:
                        if self._logger:
                            self._logger.info(f'{tag}, {operation} - {status} {reason}')
                    # For non-empty response to GET, ensure valid JSON
                    try:
                        if method == 'GET' and response.content.strip():
                            response.json()
                        return response
                    except json.decoder.JSONDecodeError as e:
                        if self._logger:
                            self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                        time.sleep(1)
                        retries -= 1
                        if retries == 0:
                            raise APIError(metadata, response)
                        else:
                            continue

                # Rate limit 429 errors
                elif status == 429:
                    if 'Retry-After' in response.headers:
                        wait = int(response.headers['Retry-After'])
                    else:
                        wait = random.randint(1, self._retry_429_wait_time)
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in {wait} seconds')
                    time.sleep(wait)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)

                # 500 errors
                elif status >= 500:
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in 1 second')
                    time.sleep(1)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)

                # 400 errors
                else:
                    if method == 'HEAD':
                        return response
                    try:
                        message = response.json()
                    except ValueError:
                        message = response.content[:100]

                    if self._retry_400_error:
                        wait = random.randint(1, self._retry_400_error_wait_time)
                        if self._logger:
                            self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in {wait} seconds')
                        time.sleep(wait)
                        retries -= 1
                        if retries == 0:
                            raise APIError(metadata, response)

                    # All other client-side errors
                    else:
                        if self._logger:
                            self._logger.error(f'{tag}, {operation} - {status} {reason}, {message}')
                        raise APIError(metadata, response)

    def get(self, metadata, url, params=None):
        metadata['method'] = 'GET'
        metadata['url'] = url
        metadata['params'] = params
        response = self.request(metadata, 'GET', url, params=params)
        ret = None
        if response:
            if isinstance(response.content, bytes) and 'data' in metadata:
                ret = response.content
            elif response.content.strip():
                ret = response.json()
            response.close()
        return ret
    
    def head(self, metadata, url):
        metadata['method'] = 'HEAD'
        metadata['url'] = url
        response = self.request(metadata, 'HEAD', url)
        ret = None
        if response:
            if response.status_code == 200:
                ret = True
            response.close()
        else:
            ret = False
        return ret

    def post(self, metadata, url, json=None, data=None):
        metadata['method'] = 'POST'
        metadata['url'] = url
        metadata['json'] = json
        metadata['data'] = data
        response = self.request(metadata, 'POST', url, json=json, data=data)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def put(self, metadata, url, json=None, data=None):
        metadata['method'] = 'PUT'
        metadata['url'] = url
        metadata['json'] = json
        metadata['data'] = data
        response = self.request(metadata, 'PUT', url, json=json, data=data)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def delete(self, metadata, url):
        metadata['method'] = 'DELETE'
        metadata['url'] = url
        response = self.request(metadata, 'DELETE', url)
        if response:
            response.close()
        return None