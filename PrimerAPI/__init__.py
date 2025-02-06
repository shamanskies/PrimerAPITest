import os
import logging
import datetime
from PrimerAPI.rest_session import *
from PrimerAPI.exceptions import *
from PrimerAPI.api.searchservice import *
from PrimerAPI.api.uploadservice import *
from PrimerAPI.config import *

# import env variables
'''
JWT = os.getenv('JWT')
DEFAULT_BASE_URL = os.getenv('DEFAULT_BASE_URL')
RETRY_429_RATE_LIMIT = os.getenv('RETRY_429_RATE_LIMIT')
RETRY_429_WAIT_TIME = os.getenv('RETRY_429_WAIT_TIME')
RETRY_400_ERROR = os.getenv('RETRY_400_ERROR'),
RETRY_400_ERROR_WAIT_TIME = os.getenv('RETRY_400_ERROR_WAIT_TIME')
MAX_RETRIES = os.getenv('MAX_RETRIES')
OUTPUT_LOG = os.getenv('OUTPUT_LOG')
LOG_PATH = os.getenv('LOG_PATH')
LOG_FILE_PREFIX = os.getenv('LOG_FILE_PREFIX')
PRINT_TO_CONSOLE = os.getenv('PRINT_TO_CONSOLE')
SUPPRESS_LOGGING = os.getenv('SUPPRESS_LOGGING')
INHERIT_LOGGING_CONFIG = os.getenv('INHERIT_LOGGING_CONFIG')
SIMULATE_API_CALLS = os.getenv('SIMULATE_API_CALLS')
'''

__version__ = '0.0.1'


def getJWT(secretsMgrMode,jwt=None):  #Add code for AUTH mechanism here
    if jwt is None:
        if secretsMgrMode:
            pass
            #ADD CODE TO GET SECRETS FROM SECRETE MANAGER..ETC

        else: #get secrets from env variables (not recommended)
            secret_key = os.environ.get("SECRET_KEY")
            secret_access_key = os.environ.get("SECRET_ACCESS_KEY")

            #ADD SSO PROVIDER INTERGRATION HERE TO GET JWT

            #return JWT
    else: #user generated JWT
        return jwt

class PrimerAPI(object):
    """
    **Creates a persistent API session**
    - jwt (string): jwt required to communicate w/ Primer API, can be entered in .env file in JWT variable or obtained with xxx FN
    - base_url (string): base url for Primer instance
    """

    def __init__(self,
                 jwt=JWT,
                 base_url=DEFAULT_BASE_URL,
                 retry_429_rate_limit=RETRY_429_RATE_LIMIT, #retry_429_rate_limit
                 retry_429_wait_time=RETRY_429_WAIT_TIME,
                 retry_400_error=RETRY_400_ERROR,
                 retry_400_error_wait_time=RETRY_400_ERROR_WAIT_TIME,
                 maximum_retries=MAX_RETRIES,
                 output_log=OUTPUT_LOG,
                 log_path=LOG_PATH,
                 log_file_prefix=LOG_FILE_PREFIX,
                 print_console=PRINT_TO_CONSOLE,
                 suppress_logging=SUPPRESS_LOGGING,
                 inherit_logging_config=INHERIT_LOGGING_CONFIG,
                 simulate=SIMULATE_API_CALLS,
                 ):
        
        # Check JWT
        #JWT = JWT or ADD FX CALL TO GET JWT
        #if not jwt:
        #    print(jwt)
        #    raise APIKeyError()

        # Configure logging
        if not suppress_logging:
            self._logger = logging.getLogger(__name__)

            if not inherit_logging_config:
                self._logger.setLevel(logging.DEBUG)

                formatter = logging.Formatter(
                    fmt='%(asctime)s %(name)12s: %(levelname)8s > %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler_console = logging.StreamHandler()
                handler_console.setFormatter(formatter)

                if output_log:
                    if log_path and log_path[-1] != '/':
                        log_path += '/'
                    self._log_file = f'{log_path}{log_file_prefix}_log__{datetime.now():%Y-%m-%d_%H-%M-%S}.log'
                    handler_log = logging.FileHandler(
                        filename=self._log_file
                    )
                    handler_log.setFormatter(formatter)

                if output_log and not self._logger.hasHandlers():
                    self._logger.addHandler(handler_log)
                    if print_console:
                        handler_console.setLevel(logging.INFO)
                        self._logger.addHandler(handler_console)
                elif print_console and not self._logger.hasHandlers():
                    self._logger.addHandler(handler_console)
        else:
            self._logger = None

        # Creates the API session to pass into service object calls
        self._session = RestSession(
            logger=self._logger,
            JWT=jwt,
            base_url=base_url,
            retry_429_rate_limit=retry_429_rate_limit,
            retry_429_wait_time=retry_429_wait_time,
            retry_400_error=retry_400_error,
            retry_400_error_wait_time=retry_400_error_wait_time,
            maximum_retries=maximum_retries,
            simulate=simulate
        )

        # API endpoints by section
        self.searchservice = SearchService(self._session)
        self.uploadservice = UploadService(self._session)
        #self.modelservice = ModelService(self._session) UPDATE THIS ONCE WE HAVE ENDPOINTS FOR TRITON READY
        