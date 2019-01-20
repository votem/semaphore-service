# Semaphore Service

## Overview

The Semaphore Service provides an HTTP REST API that allows coordination of operations
between distributed clients. Usage is simple:

### Acquire

Use the following endpoint to acquire a semaphore:

`GET /<semaphore-id>?timeout=<timeout-in-sec>`

A 204 will be returned if the semaphore is acquired successfully, or 403 if it is unavailable.
The `timeout` parameter defaults to 300 seconds, and is used to auto-release the semaphore if
a client does not do so in the given amount of time.

### Release

Use the following call to release a semaphore:

`DELETE /<semaphore-id>`

A 204 will be returned if the semaphore is released successfully, a 403 if the client does
not currently have the semaphre acquired, and a 404 if the semaphore does not exist.

## To-Do

*   Dockerize on port 80 and deploy somewhere with a real domain name
*   deal with potential race condition in GET and DELETE (current way is single-threaded bottle server)
*   create a requestor ID (hash user agent + IP or some such thing) to protect DELETEs and otherwise track requestors
*   allow true counting semaphores (count specified at creation time)
*   allow specification of timeout via query parameter when getting
*   durable semaphore storage (redis?)

## Credits

This software was developed as an internal project at Votem Corp.

Votem bolsters trust, access, and transparency in elections with a core suite
of products spanning voter registration, mobile and electronic ballot marking
for military and overseas voters and voters with accessibility considerations,
and election management systems focused on security and verifiable voting.

For more information, visit https://votem.com.
