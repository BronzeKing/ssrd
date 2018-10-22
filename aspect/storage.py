from __future__ import absolute_import

from datetime import datetime

from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils._os import safe_join
from django.utils.deconstruct import deconstructible
from storages.utils import setting

from ssrd.users.filebrowser import FileBrowser

DATE_FORMAT = '%a, %d %b %Y %X +0000'


class DropBoxFile(File):
    def __init__(self, name, storage):
        self.name = name
        self._storage = storage

    @property
    def file(self):
        if not hasattr(self, '_file'):
            self._file = self._storage.client.files_download(self.name)
        return self._file


@deconstructible
class FileBrowserStorage(Storage):
    """FileBrowser Storage class for Django pluggable storage system."""
    root_path = ''

    def __init__(self, oauth2_access_token=None, root_path=None):
        self.client = FileBrowser

    def _full_path(self, name):
        if name == '/':
            name = ''
        return safe_join(self.root_path, name).replace('\\', '/')

    def delete(self, name):
        self.client.deleteFile(self._full_path(name))

    def exists(self, name):
        try:
            return bool(self.client.getFile(self._full_path(name)))
        except ValueError:
            return False

    def listdir(self, path):
        directories, files = [], []
        full_path = self._full_path(path)
        metadata = self.client.getFiles(full_path)
        for entry in metadata['items']:
            if entry['isDir']:
                directories.append(entry['path'])
            else:
                files.append(entry['path'])
        return directories, files

    def size(self, name):
        response = self.client.getFileMeta(name)
        return response['size']

    def modified_time(self, name):
        response = self.client.getFileMeta(name)
        return response['modified']

    def accessed_time(self, name):
        response = self.client.getFileMeta(name)
        return response['modified']

    def url(self, name):
        media = self.client.files_get_temporary_link(self._full_path(name))
        return media.link

    def _open(self, name, mode='rb'):
        remote_file = self.client.getFile(name)
        return remote_file

    def _save(self, name, content):
        self.client.createFile(name, content)
        return name
