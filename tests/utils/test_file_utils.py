from __future__ import unicode_literals

from django.test.testcases import TestCase
from django_core.utils.file_utils import FilePathInfo


class FilePathInfoTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(FilePathInfoTestCase, cls).setUpClass()
        cls.file_path = '/some path/to/my_file.txt'
        cls.file_name = 'my_file.txt'
        cls.file_extension = 'txt'
        cls.file_name_without_extension = 'my_file'
        cls.file_path_without_extension = '/some path/to/my_file'
        cls.file_path_without_name = '/some path/to/'
        cls.path_info = FilePathInfo(file_path=cls.file_path)

    def test_file_path_extension(self):
        """Test file extension is correctly parsed from a file path."""
        self.assertEqual(self.path_info.file_extension, self.file_extension)

    def test_file_name(self):
        """Test file name is correctly parsed from a file path."""
        self.assertEqual(self.path_info.file_name, self.file_name)

    def test_file_name_without_extension(self):
        """Test file name without extension is correctly parsed from a file
        path."""
        self.assertEqual(self.path_info.file_name_without_extension,
                         self.file_name_without_extension)

    def test_file_path_without_extension(self):
        """Test file path without extension is correctly parsed from a file
        path."""
        self.assertEqual(self.path_info.file_path_without_extension,
                         self.file_path_without_extension)

    def test_file_path_without_name(self):
        """Test file path without name is correctly parsed from a file
        path."""
        self.assertEqual(self.path_info.file_path_without_name,
                         self.file_path_without_name)

    def test_file_path_info_from_url(self):
        """Test file path from url."""
        url = 'http://somepath.com/to/a/file.jpg?some=queryparam'
        path_info = FilePathInfo(url)

        self.assertEqual(path_info.file_extension, 'jpg')
        self.assertEqual(path_info.file_name, 'file.jpg')

    def test_file_path_info_with_multiple_extensions(self):
        """Test for getting a file name that has multiple end extensions."""
        path = '/some/path/the.filename.txt.txt'
        path_info = FilePathInfo(file_path=path)
        # this has an extension because the filename had multiple extensions
        self.assertEqual(path_info.file_name_without_extension,
                         'the.filename.txt')
