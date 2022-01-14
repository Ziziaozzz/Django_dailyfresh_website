from django.core.files.storage import Storage
from fdfs_client.client import *
from django.conf import settings


class FDFSStorage(Storage):

    def __init__(self, client_conf=None, domain=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if domain is None:
            domain = settings.FDFS_STORAGE_URL
        self.domain = domain

    def _open(self, name, mode="rb"):
        pass

    def _save(self, name, content):
        trackers = get_tracker_conf(self.client_conf)
        client = Fdfs_client(trackers)
        res = client.upload_appender_by_buffer(content.read())
        if res.get("Status") != "Upload successed.":
            raise Exception("Fail to upload")
        filename = res.get("Remote file_id")
        return filename.decode()

    def exists(self, name):
        return False

    def url(self, name):
        return self.domain + name
