# `0.4.0` Plan
Currently `0.4.0` is just meant to be the big User side update, it will also add a lot of new endpoints and events including **Client**

# `0.3.0`

## BREAKING:
Most changes this Version were breaking because of the rewrite.

HTTPClient was changed to RESTClient, Error handling moved.

REST And WebSocket events and requests are both now done through **event_factory.py** & **rest_factory.py**

HTTPClient had a rewrite, removing both the Route class and if_json class.

Client was removed during the rewrite to focus on REST and WebSocket connections, it shall be added back once we are done with both.
