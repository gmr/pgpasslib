"""
Tests for pgpasslib

"""
import mock
import os
from os import path
import stat
import tempfile
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pgpasslib


MOCK_CONTENT = """\
# This is a test entry
localhost:5432:*:kermit:

# Old entry
# bouncer:6000:*:rubber:buggy

bouncer:6000:*:rubber:buggy

# Another Test
foo.abjdite.us-east-1.redshift.amazonaws.com:5439:*:fonzy:b3ar
foo\:bar:6000:*:baz:qux
"""


class ReadFileOpenTest(unittest.TestCase):

    def test_open_arguments(self):
        with mock.patch('pgpasslib._file_path') as _file_path:
            with mock.patch('pgpasslib.open',
                            mock.mock_open(read_data='baz'),
                            create=True) as mock_open:
                _file_path.return_value = '/tmp/foo.bar'
                pgpasslib._read_file()
                mock_open.assert_called_once_with('/tmp/foo.bar', 'r')


class ReadFileReturnValueTest(unittest.TestCase):

    def test_returns_file_contents(self):
        with mock.patch('pgpasslib._file_path') as _file_path:
            with mock.patch('pgpasslib.open',
                            mock.mock_open(read_data='baz'),
                            create=True):
                _file_path.return_value = '/tmp/foo.bar'
                self.assertEqual(pgpasslib._read_file(), 'baz')


class GetEntriesTest(unittest.TestCase):

    def test_return_values_with_mock_content(self):
        expectation = [('localhost', 5432, '*', 'kermit', ''),
                       ('bouncer', 6000, '*', 'rubber', 'buggy'),
                       ('foo.abjdite.us-east-1.redshift.amazonaws.com', 5439,
                        '*', 'fonzy', 'b3ar'),
                       ('foo:bar', 6000, '*', 'baz', 'qux')]
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            result = [(e.host, e.port, e.dbname, e.user, e.password)
                      for e in pgpasslib._get_entries()]
            self.assertListEqual(result, expectation)


class DefaultPathTests(unittest.TestCase):

    def test_path_matches_expectation(self):
        self.assertEqual(pgpasslib._default_path(),
                         path.join(path.expanduser('~'), '.pgpass'))


class FilePathNotFoundTest(unittest.TestCase):

    def test_filenotfound_is_raised(self):
        os.environ['PGPASSFILE'] = '/foo/bar/baz/qux/.pgpass'
        self.assertRaises(pgpasslib.FileNotFound, pgpasslib._file_path)


class FilePathInvalidPermissionTest(unittest.TestCase):

    def test_invalidpermissions_is_raised(self):
        with tempfile.NamedTemporaryFile(delete=False) as file_handle:
            file_handle.write(b'foo\n')
            file_name = file_handle.name
        os.environ['PGPASSFILE'] = file_name
        os.chmod(file_name,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        with self.assertRaises(pgpasslib.InvalidPermissions):
            pgpasslib._file_path()
        os.remove(file_name)

    def test_invalidpermissions_is_not_raised_on_windows(self):
        with tempfile.NamedTemporaryFile(delete=False) as file_handle:
            file_handle.write(b'foo\n')
            file_name = file_handle.name
        os.environ['PGPASSFILE'] = file_name
        os.chmod(file_name,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        with mock.patch('platform.system') as system:
            system.return_value = 'Windows'
            value = pgpasslib._file_path()
        self.assertEqual(value, file_name)
        os.remove(file_name)


class FilePathValidPermissionTest(unittest.TestCase):

    def test_valid_permissions_return_path(self):
        with tempfile.NamedTemporaryFile(delete=False) as file_handle:
            file_handle.write(b'foo\n')
            file_name = file_handle.name
        os.environ['PGPASSFILE'] = file_name
        os.chmod(file_name, stat.S_IRUSR)
        self.assertEqual(pgpasslib._file_path(), file_name)
        os.remove(file_name)


class EntryCreationTest(unittest.TestCase):

    def setUp(self):
        self.entry = pgpasslib._Entry('foo', 1234, 'bar', 'baz', 'qux')

    def test_host_attribute(self):
        self.assertEqual(self.entry.host, 'foo')

    def test_port_attribute(self):
        self.assertEqual(self.entry.port, 1234)

    def test_dbname_attribute(self):
        self.assertEqual(self.entry.dbname, 'bar')

    def test_user_attribute(self):
        self.assertEqual(self.entry.user, 'baz')

    def test_password_attribute(self):
        self.assertEqual(self.entry.password, 'qux')


class EntryInvalidHostTest(unittest.TestCase):

    def test_invalid_entry_is_raised(self):
        self.assertRaises(pgpasslib.InvalidEntry, pgpasslib._Entry,
                          123, 'bar', 'baz', 'qux', 'corgie')


class EntryInvalidPortTest(unittest.TestCase):

    def test_invalid_entry_is_raised(self):
        self.assertRaises(pgpasslib.InvalidEntry, pgpasslib._Entry,
                          'foo', 'bar', 'baz', 'qux', 'corgie')


class EntryAllWildcardsButHostMatchTest(unittest.TestCase):

    def setUp(self):
        self.entry = pgpasslib._Entry('foo', '*', '*', '*', 'pass')

    def test_match_on_host(self):
        self.assertTrue(self.entry.match('foo', 5432, 'bar', 'baz'))

    def test_no_match_on_host(self):
        self.assertFalse(self.entry.match('fooz', 5432, 'bar', 'baz'))


class EntryAllWildcardsButPortMatchTest(unittest.TestCase):

    def setUp(self):
        self.entry = pgpasslib._Entry('*', 5432, '*', '*', 'pass')

    def test_match_on_host(self):
        self.assertTrue(self.entry.match('foo', 5432, 'bar', 'baz'))

    def test_no_match_on_host(self):
        self.assertFalse(self.entry.match('foo', 6000, 'bar', 'baz'))


class EntryAllWildcardsButDBNameMatchTest(unittest.TestCase):

    def setUp(self):
        self.entry = pgpasslib._Entry('*', '*', 'bar', '*', 'pass')

    def test_match_on_host(self):
        self.assertTrue(self.entry.match('foo', 5432, 'bar', 'baz'))

    def test_no_match_on_host(self):
        self.assertFalse(self.entry.match('foo', 6000, 'qux', 'baz'))


class EntryAllWildcardsButUserMatchTest(unittest.TestCase):

    def setUp(self):
        self.entry = pgpasslib._Entry('*', '*', '*', 'baz', 'pass')

    def test_match_on_host(self):
        self.assertTrue(self.entry.match('foo', 5432, 'bar', 'baz'))

    def test_no_match_on_host(self):
        self.assertFalse(self.entry.match('foo', 6000, 'bar', 'qux'))


class GetPassMatch1Test(unittest.TestCase):

    def test_getpass_returns_expected_result(self):
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            self.assertEqual(pgpasslib.getpass('localhost', 5432,
                                               'foo', 'kermit'), '')


class GetPassMatch2Test(unittest.TestCase):

    def test_getpass_returns_expected_result(self):
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            self.assertEqual(pgpasslib.getpass('bouncer', 6000,
                                               'bumpers', 'rubber'), 'buggy')


class GetPassMatch3Test(unittest.TestCase):

    def test_getpass_returns_expected_result(self):
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            self.assertEqual(pgpasslib.getpass('foo.abjdite.us-east-1.'
                                               'redshift.amazonaws.com', 5439,
                                               'redshift', 'fonzy'), 'b3ar')


class GetPassMatch4Test(unittest.TestCase):

    def test_getpass_returns_expected_result(self):
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            self.assertEqual(pgpasslib.getpass('foo:bar', '6000',
                                               'corgie', 'baz'), 'qux')


class GetPassNoMatchTest(unittest.TestCase):
    def test_path_matches_expectation(self):
        with mock.patch('pgpasslib._read_file') as read_file:
            read_file.return_value = MOCK_CONTENT
            self.assertRaises(pgpasslib.NoMatchingEntry,
                              lambda: pgpasslib.getpass('fail', '5432', 'foo',
                                                        'bar'))


class NoMatchingEntryStrFormatting(unittest.TestCase):
    def test_str_matches_expectation(self):
        msg = "host=fail; port=5432; dbname=foo; user=bar"
        self.assertEqual(str(pgpasslib.NoMatchingEntry(msg)),
                         'No match for connection entry "%s"' % msg)


class FileNotFoundStrFormatting(unittest.TestCase):

    def test_str_matches_expectation(self):
        self.assertEqual(str(pgpasslib.FileNotFound('.pgpass')),
                         'No such file ".pgpass"')


class InvalidEntryExceptionStrFormatting(unittest.TestCase):

    def test_str_matches_expectation(self):
        self.assertEqual(str(pgpasslib.InvalidEntry('host', 1234)),
                         'Error validating host value "1234"')


class InvalidPermissionsExceptionStrFormatting(unittest.TestCase):

    def test_str_matches_expectation(self):
        self.assertEqual(str(pgpasslib.InvalidPermissions('foo', '0x000')),
                         'Invalid Permissions for foo: 0x000')
