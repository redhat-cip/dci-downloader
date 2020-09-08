import os
import fcntl
import sys


if sys.version_info[0] == 3:
    LOCK_IO_ERROR = BlockingIOError  # noqa: F821
else:
    LOCK_IO_ERROR = IOError


class LockError(Exception):
    pass


class file_lock(object):
    lock_fd = None

    def __init__(self, file_path):
        print("__init__")
        try:
            print("Try go get file descriptor on %s" % file_path)
            lock_fd = open(file_path, "r+")
        except IOError:
            print("IOError file doesn't exist, open in a+ mode to create it")
            lock_fd = open(file_path, "a+")
        try:
            print("flock %s" % file_path)
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except LOCK_IO_ERROR:
                print("LOCK_IO_ERROR")
                raise LockError("Couldn't lock %s" % file_path)
            self.lock_fd = lock_fd
        except:  # noqa
            print("Close file %s" % file_path)
            lock_fd.close()
            raise

    def __enter__(self):
        print("__enter__")
        return self.lock_fd

    def __exit__(self, type, value, traceback):
        print("__exit__")
        if self.lock_fd is not None:
            print("self.lock_fd is not None")
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            self.lock_fd.close()
            try:
                os.remove(self.lock_fd.name)
            except OSError:
                print("Strange issue can't remove %s (OSError)" % self.lock_fd.name)
            self.lock_fd = None
