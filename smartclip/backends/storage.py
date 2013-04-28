from StringIO import StringIO

from django.core.files.base import ContentFile
from django.core.files.storage import Storage

from .smartfile_backend import SmartfileClient


class SmartfileStorage(Storage):
    def __init__(self, client_token=None, client_secret=None, *args, **kwargs):
        self.client = SmartfileClient(client_token=client_token,
                                      client_secret=client_secret,
                                      access_token=access_token,
                                      access_secret=access_secret)

    def save(self, name, content):
        # 'name' == 'filename' property
        # 'content' == SmartfileFile instance
        path = 'smartclip.%s' % content.type
        if not self.exists(path):
            self.client.post('/path/oper/mkdir', path='/%s' % path)
            
        self.client.post('/path/data/smartclip/%s' % content.type,
                         file=(name, content.file.read()))
        content.file.seek(0)

    def exists(self, name):
        name = '/path/data/info/%s' % name
        response = api.client.get(name)

        if response.status_code == 200:
            return True
        else:
            return False
        

class SmartfileFile(ContentFile):
    def __init__(self, name, content, _type):
        # 'type' is either 'pdf' or 'html'
        self.name = name
        self.file = StringIO(content.encode('utf-8'))
        self.type = _type
        self.is_dirty = False

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, content):
        self.file = StringIO(content)
        self.is_dirty = True

    def close(self):
        if self.is_dirty:
            self.client.post('/path/data/smartclip/%s' % self.type,
                             file=(self.name, self.file))
        self.file.close()
