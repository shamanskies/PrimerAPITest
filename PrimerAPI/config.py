##################################
# Configure constants to setup API
# endpoint for usage
#
#
#
#
##################################

# set web token - this is temporary until keycloak or other method is implemented
JWT = "INSERT TOKEN HERE"

# Base URL preceding all endpoint resources
DEFAULT_BASE_URL = 'https://delta-api.primer.ai/' #modify this based on endpoint WILL ONLY WORK FOR D3 ENVIRONMENT

# Maximum number of seconds for each API call
SINGLE_REQUEST_TIMEOUT = 60

# Retry if 429 rate limit error encountered?
RETRY_429_RATE_LIMIT = True

# Nginx 429 retry wait time
RETRY_429_WAIT_TIME = 60

# Action batch concurrency error retry wait time
ACTION_BATCH_RETRY_WAIT_TIME = 60

# Retry if encountering other 400 type errors (besides 429)?
RETRY_400_ERROR = False

# Other 400 error retry wait time
RETRY_400_ERROR_WAIT_TIME = 60

# Sets max retries for any errors
MAX_RETRIES = 2

# Create an output log file?
OUTPUT_LOG = True

# Logs to working dir unless alternate directory is specified here
LOG_PATH = ''

# Log file name appended with date and timestamp
LOG_FILE_PREFIX = 'primerapi_test_' #change this to something else once implemented

# Print output logging to console?
PRINT_TO_CONSOLE = True

# Option to disable logging
SUPPRESS_LOGGING = False

# You might integrate the library in an application with a predefined logging scheme. If so, you may not need the
# library's default logging handlers, formatters etc.--instead, you can inherit an external logger instance.
INHERIT_LOGGING_CONFIG = False

# Simulate POST/PUT/DELETE calls to prevent changes?
SIMULATE_API_CALLS = False

# Optional identifier for API usage tracking; (PRIMER_API_CALLER)
PRIMER_API_CALLER = ''