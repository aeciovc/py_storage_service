import base64
import json

class File(object):

    def __init__(self, content):
        self.content = content

    #Decode content from base64
    def decode(self):
        return base64.b64decode(self.content)

    #Encode content to base64
    def encode(self):
        base64_bytes = base64.b64encode(self.content)
        self.content = base64_bytes.decode('utf-8')
        return self

    def as_dict(self):
        return dict(
            content=self.content)

    def as_json(self):
        return json.dumps(self.as_dict())