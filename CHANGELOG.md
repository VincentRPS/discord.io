# `0.4.0` Plan
Currently `0.4.0` is just meant to be the big User side update, it will also add a lot of new endpoints and events including **Client**

rpd.Color and rpd.Colour would be added to help with colors.

# `0.3.0`
Most changes this Version were breaking because of the rewrite.

## BREAKING:

HTTPClient was changed to RESTClient, Error handling moved.

REST And WebSocket events and requests are both now done through **event_factory.py** & **rest_factory.py**

HTTPClient had a rewrite, removing both the Route class and if_json class.

Client was removed during the rewrite to focus on REST and Gateway connections, it shall be added back once we are done with both.

rpd.Intents has been added to calculate intents easier.

rpd.helpers was moved to rpd.util
