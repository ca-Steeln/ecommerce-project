
from django.utils.deprecation import MiddlewareMixin
from django.contrib.messages import get_messages
from json import dumps, loads

class HtmxMessagesMiddleware(MiddlewareMixin):

    def process_response(self, request, respose):

        hx_trigger = respose.headers.get('HX-Trigger')
        if hx_trigger is not None:
            try:
                hx_trigger = loads(hx_trigger)
            except:
                hx_trigger = {hx_trigger: True}
        else:
            hx_trigger = {}

        hx_trigger['messages'] = [
            {
                "message": message.message,
                "tags": message.tags,
            }
            for message in get_messages(request)
        ]

        respose.headers['HX-Trigger'] = dumps(hx_trigger)

        return respose
