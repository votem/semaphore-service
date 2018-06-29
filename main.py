#!/usr/bin/env python3


# Standard library imports
import datetime
import logging

# Additional library imports
import bottle


# Configure the logging module.
logformat = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
logging.basicConfig(format=logformat, level=logging.INFO)


# If a semaphore is not released within this time in seconds, it is automatically released.
DEFAULT_TIMEOUT = 300


# Semaphore data is stored in a simple dictionary.
SEMAPHORES = {}


# Ensure no requests are ever cached.
@bottle.hook('after_request')
def _setdefaultheaders():
    bottle.response.set_header('Cache-Control', 'no-cache')


@bottle.get('/<semaphoreid>')
def _getsemaphore(semaphoreid):
    """
    Acquire a semphore; if the ID does not exist, it is created.
    @param semaphoreid: Uniquely identifies the particular semaphore to acquire
    @return: 204 NO CONTENT if the semaphore is acquired successfully
             403 FORBIDDEN if the semaphore is not available
             500 INTERNAL SERVER ERROR if an unknown problem occurs
    """
    semaphore = SEMAPHORES.get(semaphoreid, {'id': semaphoreid, 'expiry': datetime.datetime.min})
    SEMAPHORES[semaphoreid] = semaphore
    currenttime = datetime.datetime.now()
    if currenttime > semaphore['expiry']:
        timeout = bottle.request.get('timeout', DEFAULT_TIMEOUT)
        semaphore['expiry'] = currenttime + datetime.timedelta(seconds=timeout)
        logging.info('Semaphore "{0}" acquired'.format(semaphoreid))
        bottle.response.status = 204
    else:
        bottle.abort(403, 'Semaphore "{0}" is not available'.format(semaphoreid))


@bottle.delete('/<semaphoreid>')
def _deletesemaphore(semaphoreid):
    """
    Release a semphore.
    @param semaphoreid: Uniquely identifies the particular semaphore to release
    @return: 204 NO CONTENT if the semaphore is released successfully
             403 FORBIDDEN if the caller has not yet acquired the semaphore
             404 NOT FOUND if the semaphore does not exist
             500 INTERNAL SERVER ERROR if an unknown problem occurs
    """
    try:
        del SEMAPHORES[semaphoreid]
        logging.info('Semaphore "{0}" released'.format(semaphoreid))
        bottle.response.status = 204
    except KeyError:
        bottle.abort(404, 'Semaphore "{0}" does not exist'.format(semaphoreid))


@bottle.error(400)
@bottle.error(403)
@bottle.error(404)
@bottle.error(500)
def _error(error):
    """
    Log errors for all potential HTTP bad codes.
    @param error: The error message from an above function
    """
    logging.info(error.body)


# Start the HTTP server.
logging.info('Starting HTTP server')
bottle.run(host='0.0.0.0', quiet=True)
