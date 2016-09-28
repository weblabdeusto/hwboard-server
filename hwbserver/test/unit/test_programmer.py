
import unittest
import mock
from mock import patch
import time

from programmer import Programmer

def program_file_instant(self, content):
    pass

def program_file_slow(self, content):
    time.sleep(0.5)

def program_file_error(self, content):
    raise Exception("Exception for test")


class TestProgrammer(unittest.TestCase):

    def test_programmer_initially_ready(self):
        pr = Programmer()
        self.assertFalse(pr.is_programming())

    @patch.object(Programmer, '_program_file_impl', program_file_slow)
    def test_programmer_programming(self):
        pr = Programmer()

        def on_success():
            pass
        def on_error(ex):
            pass
        pr.program_file("FILE CONTENT SLOW", on_success, on_error)

        self.assertTrue(pr.is_programming())

    @patch.object(Programmer, '_program_file_impl', program_file_slow)
    def test_programming_success(self):

        pr = Programmer()
        track = {
            'success': False,
            'error': False
        }
        def on_success():
            track['success'] = True
        def on_error(ex):
            track['error'] = True

        pr.program_file("FILE CONTENT SUCCESS", on_success, on_error)

        # Wait until success is set to True on the secondary thread.
        start_checking = time.time()
        while time.time() - start_checking < 2:
            if not pr.is_programming():
                break

        self.assertTrue(track['success'])
        self.assertFalse(track['error'])

    @patch.object(Programmer, '_program_file_impl', program_file_error)
    def test_programming_error(self):
        pr = Programmer()
        track = {
            'success': False,
            'error': False
        }
        def on_success():
            track['success'] = True
        def on_error(ex):
            track['error'] = True

        pr.program_file("FILE CONTENT ERROR", on_success, on_error)

        # Wait until success is set to True on the secondary thread.
        start_checking = time.time()
        while time.time() - start_checking < 2:
            if track['error']:
                break

        self.assertTrue(track['error'])
        self.assertFalse(track['success'])

    def test_programming_success_twice(self):

        pr = Programmer()
        track = {
            'success': 0,
            'error': 0
        }

        def on_success():
            track['success'] += 1
        def on_error(ex):
            track['error'] += 1

        pr.program_file("FILE CONTENT SUCCESS", on_success, on_error)

        # Wait until success is set to True on the secondary thread.
        start_checking = time.time()
        while time.time() - start_checking < 2:
            if not pr.is_programming():
                break

        pr.program_file("FILE CONTENT SUCCESS", on_success, on_error)

        # Wait until success is set to True on the secondary thread.
        start_checking = time.time()
        while time.time() - start_checking < 2:
            if not pr.is_programming():
                break

        self.assertEquals(track['success'], 2)
        self.assertEquals(track['error'], 0)


if __name__ == '__main__':
    unittest.main()
