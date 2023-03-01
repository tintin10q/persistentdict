import os
import time
import json
import copy
import typing
from collections import UserDict
from multiprocessing import Lock


class Format:
    """A class that represents a format that can be used to save and load a dictionary."""

    def dump(self, data, file: typing.TextIO, **dump_kwargs):
        raise NotImplemented("You must implement the dump method for your format.")

    def load(self, file: typing.TextIO) -> dict:
        raise NotImplemented("You must implement the load method for your format.")

    __name__: str = "unknown"


FormatT = typing.TypeVar("FormatT", bound=Format)


class persistentdict(UserDict):
    """A dictionary that persists to a file on disk."""
    __locks = {}  # A dictionary of locks for each file.
    default_backup_path = os.path.join(os.path.dirname(__file__), "backups")

    def __init__(self, filename: str, format: FormatT = json, using_locks: bool = False, **dump_kwargs):
        """
            A dictionary that persists to a file on disk.
            :param filename: The file to save the dictionary to.
            :param format=json: The format to save the dictionary in. Should be a class that has a dump and load method and __name__.
            :param using_locks: If True, the dictionary will be locked when it is being read or written to. This is useful if you are using multiple processes to access the dictionary.
            :param dump_kwargs: Any keyword arguments to pass to the dump method of the format.
        """
        super().__init__()
        self.__filename = filename
        self.__in_with = False
        self.format = format
        self.using_locks = using_locks
        self.dump_kwargs = dump_kwargs
        self.backup_path = persistentdict.default_backup_path
        if self.format_name == 'json':
            self.dump_kwargs["indent"] = 2

    @property
    def format_name(self):
        return self.format.__name__

    @property
    def filename(self):
        return self.__filename + f".{self.format.__name__}"

    def lock(self):
        """
        Locks the file if it is using_locks and not already locked by us.
        :param self:
        :return:
        """
        if not self.using_locks or self.__in_with:
            return
        if self.filename not in self.__locks:
            persistentdict.__locks[self.filename] = Lock()
        persistentdict.__locks[self.filename].acquire()

    def unlock(self):
        """
        Unlocks the file if it is using_locks and not already locked by us.
        :param self:
        """
        if not self.using_locks:
            return
        persistentdict.__locks[self.filename].release()

    def __enter__(self):
        self.lock()
        self.__in_with = True  # should happen after lock
        self.load()
        self.__backup_data = copy.deepcopy(self.data)  # Make a deep copy to preserve the backup and also lists inside the backup
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.dump()
            if exc_type is not None:  # There was an error in context attempt rollback
                self.restore()
        finally:
            self.unlock()
            self.__in_with = False

    def dump(self):
        with open(self.filename, 'w+') as f:
            self.format.dump(self.data, f, **self.dump_kwargs)

    def load(self):
        if not os.path.exists(self.filename):
            self.clear()
            return # Only read from file if it already exists
        with open(self.filename, 'r+') as f:
            data = self.format.load(f)
            self.data = data if data is not None else {}  # If the file is empty, make it an empty dict

    def create_backup(self):
        """
        Makes backups in a backup_path with the current date
        """
        timestring = time.strftime("-%Y%m%d-%H%M%S")

        if not os.path.exists(persistentdict.default_backup_path):
            os.mkdir(persistentdict.default_backup_path)

        backup_path = os.path.join(self.backup_path, self.filename, timestring, f".{self.format}")

        with open(backup_path, 'w+') as f:
            self.format.dump(self.data, f, **self.dump_kwargs)

    def restore(self):
        """
        Restores the data from the backup
        """
        self.data = self.__backup_data
        self.dump()
