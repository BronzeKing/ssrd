# encoding: utf-8

import io
from datetime import datetime

from django.core.exceptions import ImproperlyConfigured, SuspiciousFileOperation
from django.core.files.base import ContentFile, File
from django.test import TestCase

try:
    from unittest import mock
except ImportError:  # Python 3.2 and below
    import mock


class F(object):
    pass


FILE_DATE = datetime(2015, 8, 24, 15, 6, 41)
FILE_FIXTURE = {
    'bytes': 4,
    'client_mtime': 'Mon, 24 Aug 2015 15:06:41 +0000',
    'icon': 'page_white_text',
    'is_dir': False,
    'mime_type': 'text/plain',
    'modified': 'Mon, 24 Aug 2015 15:06:41 +0000',
    'path': '/foo.txt',
    'rev': '23b7cdd80',
    'revision': 2,
    'root': 'app_folder',
    'size': '4 bytes',
    'thumb_exists': False
}
FILES_FIXTURE = {
    'bytes': 0,
    'contents': [
        FILE_FIXTURE,
        {'bytes': 0,
         'icon': 'folder',
         'is_dir': True,
         'modified': 'Mon, 6 Feb 2015 15:06:40 +0000',
         'path': '/bar',
         'rev': '33b7cdd80',
         'revision': 3,
         'root': 'app_folder',
         'size': '0 bytes',
         'thumb_exists': False}
    ],
    'hash': 'aeaa0ed65aa4f88b96dfe3d553280efc',
    'icon': 'folder',
    'is_dir': True,
    'path': '/',
    'root': 'app_folder',
    'size': '0 bytes',
    'thumb_exists': False
}
FILE_MEDIA_FIXTURE = F()
FILE_MEDIA_FIXTURE.link = 'https://dl.dropboxusercontent.com/1/view/foo'


class DropBoxTest(TestCase):
    def setUp(self, *args):
        self.storage = dropbox.DropBoxStorage('foo')

    def test_no_access_token(self, *args):
        with self.assertRaises(ImproperlyConfigured):
            dropbox.DropBoxStorage(None)

    def test_delete(self, *args):
        self.storage.delete('foo')

    def test_exists(self, *args):
        exists = self.storage.exists('foo')
        self.assertTrue(exists)

    def test_not_exists(self, *args):
        exists = self.storage.exists('bar')
        self.assertFalse(exists)

    def test_listdir(self, *args):
        dirs, files = self.storage.listdir('/')
        self.assertGreater(len(dirs), 0)
        self.assertGreater(len(files), 0)
        self.assertEqual(dirs[0], 'bar')
        self.assertEqual(files[0], 'foo.txt')

    def test_size(self, *args):
        size = self.storage.size('foo')
        self.assertEqual(size, FILE_FIXTURE['bytes'])

    def test_modified_time(self, *args):
        mtime = self.storage.modified_time('foo')
        self.assertEqual(mtime, FILE_DATE)

    def test_accessed_time(self, *args):
        mtime = self.storage.accessed_time('foo')
        self.assertEqual(mtime, FILE_DATE)

    def test_open(self, *args):
        obj = self.storage._open('foo')
        self.assertIsInstance(obj, File)

    def test_save(self, files_upload, *args):
        self.storage._save('foo', File(io.BytesIO(b'bar'), 'foo'))
        self.assertTrue(files_upload.called)

    def test_chunked_upload(self, start, append, finish, upload):
        large_file = File(io.BytesIO(b'bar' * self.storage.CHUNK_SIZE), 'foo')
        self.storage._save('foo', large_file)
        self.assertTrue(start.called)
        self.assertTrue(append.called)
        self.assertTrue(finish.called)
        self.assertFalse(upload.called)

    def test_url(self, *args):
        url = self.storage.url('foo')
        self.assertEqual(url, FILE_MEDIA_FIXTURE.link)

    def test_formats(self, *args):
        self.storage = dropbox.DropBoxStorage('foo')
        files = self.storage._full_path('')
        self.assertEqual(files, self.storage._full_path('/'))
        self.assertEqual(files, self.storage._full_path('.'))
        self.assertEqual(files, self.storage._full_path('..'))
        self.assertEqual(files, self.storage._full_path('../..'))


class DropBoxFileTest(TestCase):
    def setUp(self, *args):
        self.storage = dropbox.DropBoxStorage('foo')
        self.file = dropbox.DropBoxFile('/foo.txt', self.storage)

    @mock.patch('dropbox.Dropbox.files_download',
                return_value=ContentFile(b'bar'))
    def test_read(self, *args):
        file = self.storage._open(b'foo')
        self.assertEqual(file.read(), b'bar')


class DropBoxRootPathTest(TestCase):
    def test_jailed(self, *args):
        self.storage = dropbox.DropBoxStorage('foo', '/bar')
        dirs, files = self.storage.listdir('/')
        self.assertFalse(dirs)
        self.assertFalse(files)

    def test_suspicious(self, *args):
        self.storage = dropbox.DropBoxStorage('foo', '/bar')
        with self.assertRaises((SuspiciousFileOperation, ValueError)):
            self.storage._full_path('..')

    def test_formats(self, *args):
        self.storage = dropbox.DropBoxStorage('foo', '/bar')
        files = self.storage._full_path('')
        self.assertEqual(files, self.storage._full_path('/'))
        self.assertEqual(files, self.storage._full_path('.'))
