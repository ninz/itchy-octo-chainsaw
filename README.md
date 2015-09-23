# Rackspace Queue Test Widgets


This is a proof of concept which consists of

 -  A [producer](widget_producer.py) which is tasked with submitting new
    requests that create widgets.

 - A [consumer](widget_consumer.py) which takes the new request and
    POSTs it to a widget maker web app.

 - A [widget maker web app](widget_maker.py) which takes the POST
   request, validates the request and creates the widget.

## Setup

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
Set up pyrax to use [keyring authentication](https://github.com/rackspace/pyrax/blob/master/docs/getting_started.md#authenticating). See https://github.com/jaraco/keyring for more info.

Create the two queues itchy-octo-chainsaw-request and itchy-octo-chainsaw-response in Rackspace.

## Run

Run the widget maker
    venv/bin/python widget_maker.py

Run the widget consumer
    venv/bin/python widget_consumer.py
    
Generate a new widget request using a randomly generated widget id.
    venv/bin/python widget_producer.py
    
Generate a new widget request with a specific valid widget id.
    venv/bin/python widget_producer.py --widget-id=31f37378-54f4-11e5-ad75-3c970e65f731
    
Generate a new widget request with an invalid widget-id.
    venv/bin/python widget_producer.py --widget-id=this_is_not_a_valid_widget_id
    



