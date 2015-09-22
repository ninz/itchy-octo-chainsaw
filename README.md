# Rackspace Queue Test Widgets


This is a proof of concept which consists of

 -  A [producer](widget_producer.py) which is tasked with submitting new
    requests that create widgets.

 - A [consumer](widget_consumer.py) which takes the new request and
    POSTs it to a widget maker web app.

 - A [widget maker web app](widget_maker.py) which takes the POST
   request, validates the request and creates the widget.

## Setup

Set up pyrax to use [keyring authentication](https://github.com/rackspace/pyrax/blob/master/docs/getting_started.md#authenticating). See https://github.com/jaraco/keyring for more info.