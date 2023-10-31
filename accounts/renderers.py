from rest_framework import renderers
import json


# class to display the any type of error occured during Login Endpoint, either blank, email/password mismatch or any...
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)

        return response