
import unittest

from programmer import Programmer


class TestProgrammer(unittest.TestCase):

    def test_programmer_initially_ready(self):
        pr = Programmer()
        self.assertFalse(pr.is_programming())

    def test_programmer_programming(self):
        pr = Programmer()
        def on_success():
            pass
        def on_error():
            pass
        pr.program_file("FILE CONTENT SLOW", on_success, on_error)

        self.assertTrue(pr.is_programming())

    # def test_programming_success(self):
    #     pr = Programmer()
    #     success_called = False
    #     error_called = False
    #     def on_success():
    #         success_called = True
    #     def on_error():
    #         error_called = False
    #
    #     pr.program_file("FILE CONTENT SCUCESS", on_success, on_error)
    #
    #     self.assertTrue(success_called)
    #     self.assertFalse(error_called)
    #
    # def test_programming_error(self):
    #
    #     def on_success():
    #         success_called = True
    #     def on_error():
    #         error_called = False
    #
    #     pr.program_file("FILE CONTENT ERROR", on_success, on_error)
    #
    #     self.assertTrue(error_called)
    #     self.assertFalse(success_called)
    #
    # def test_programming_success_twice(self):
    #     pr = Programmer()
    #     success_called = 0
    #     error_called = 0
    #     def on_success():
    #         success_called += 1
    #     def on_error():
    #         error_called += 1
    #
    #     pr.program_file("FILE CONTENT SCUCESS", on_success, on_error)
    #
    #     self.assertEquals(success_called, 2)
    #     self.assertEquals(error_called, 0)
    #
    # def test_programming_success_after_error(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
