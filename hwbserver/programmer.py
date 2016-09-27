import os
import tempfile

import time
import traceback

from voodoo.log import logged
from voodoo.threaded import threaded


class ProgrammerError(Exception):
    """
    Base exception class for every programmer error.
    """

    def __init__(self, message, errors):
        super(ProgrammerError, self).__init__(message)
        self.errors = errors


class ProgrammerNotReady(ProgrammerError):
    """
    To be raised when the programming process could not even be started due to some kind of
    error.
    """
    def __init__(self, message, errors):
        super(ProgrammerNotReady, self).__init__(message, errors)


class ProgrammingFailed(ProgrammerError):
    """
    To be raised when an error occurs after trying to program.
    """
    def __init__(self, message, errors):
        super(ProgrammingFailed, self).__init__(message, errors)


class Programmer(object):
    """
    Handles programming the logic into the physical board.
    """

    def __init__(self, debug=False):
        self._debug = debug
        self._thread_active = False
        self._success_callback = None
        self._error_callback = None

    def is_programming(self):
        """
        Checks whether we are currently programming the board already.
        :return:
        """
        return self._thread_active

    def program_file(self, file_content, success_callback, error_callback):
        """
        Programs the provided logic into the board. A running programming process must end before a new one
        can be started. Otherwise, the error callback will immediately be invoked with a ProgrammerNotReady error.

        :param file_content: Binary content to program into the board.
        :param success_callback: Callback to be invoked after success, which will be invoked ON A WORKER THREAD.
        :param error_callback: Callback to be invoked after failure, which will be invoked ON A WORKER THREAD.
        :return:
        """
        if file_content is None or len(file_content) == 0 or success_callback is None or error_callback is None:
            raise ProgrammerError("Invalid call to program_file")

        if self.is_programming():
            error = ProgrammerNotReady("Already programmming the board")
            error_callback(error)

        self._thread_active = True

        self._success_callback = success_callback
        self._error_callback = error_callback

        # This will start the thread and handle everything for this programming process from then on.
        self._program_file_t(file_content)

    def _program_file_impl(self, file_content):
        """
        Actual implementation method that will program the binaries into the board. This method should be invoked
        from a worker thread, because it may block for a relatively long time.

        TODO: This method has not yet been adapted to support the new programmer.

        :param file_content:
        :return:
        """

        try:
            fd, file_name = tempfile.mkstemp(prefix='ud_xilinx_experiment_program',
                                             suffix='.' + 'bit')

            if self._debug:
                print "[DBG]: 2"
                df2 = open("/tmp/orig_content", "w")
                df2.write("---begin---\n")
                df2.write(file_content)
                df2.close()

                # For debugging purposes write the file to tmp
                df = open("/tmp/fpga_programmer.log.dat", "w")

            try:
                try:
                    # TODO: encode? utf8?
                    if isinstance(file_content, unicode):
                        if self._debug: print "[DBG]: Encoding file content in utf8"
                        file_content_encoded = file_content.encode('utf8')
                    else:
                        if self._debug: print "[DBG]: Not encoding file content"
                        file_content_encoded = file_content

                    # TODO:
                    # file_content_recovered = ExperimentUtil.deserialize(file_content_encoded)
                    file_content_recovered = ""

                    os.write(fd, file_content_recovered)
                    if self._debug:
                        df.write(file_content_recovered)
                finally:
                    os.close(fd)

                    # TODO:
                    # self._programmer.program(file_name)
            finally:
                os.remove(file_name)
        except Exception as ex:

            if self._debug:
                tb = traceback.format_exc()
                print "FULL EXCEPTION IS: {0}".format(tb)

            raise ex

    @threaded()
    @logged("info", except_for='file_content')
    def _program_file_t(self, file_content):
        """
        Running in its own thread, this method will program the board and report success or failure through
        the callbacks that were provided during the program_board invocation.
        """
        try:
            start_time = time.time()  # To track the time it takes
            self._program_file_impl(file_content)
            elapsed = time.time() - start_time  # Calculate the time the programming process took

            if self._debug:
                print "[DBG]: Finished programming the board."

            self._success_callback()

        except Exception as ex:

            prf = ProgrammingFailed(ex)
            self._error_callback(prf)

        self._thread_active = False
