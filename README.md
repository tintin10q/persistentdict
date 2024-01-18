# persistentdict

Persistent dict is a context manager that loads and stores a dict in a file automatically. Inspired by my
[python_json_database_manager](https://github.com/tintin10q/python_json_database_manager) repo (this is just a simpler version)

For proper toml integration, you need to install toml package. The standard library toml module is not enough as it can
only load toml files but not create them. The persistant dict works with anything that implements my Format abstract base class. 
That means any object with a `dump` and `load` method and a `__name__` attribute.

## Usage

```python
from persistentdict import persistentdict

with persistentdict("test") as d:
    d["test"] = "test"
    d["test2"] = "test2"

"""
A dictionary that persists to a file on disk.
   :param filename: The file to save the dictionary to.
   :param format=json: The format to save the dictionary in. Should be a class that has a dump and load method and __name__.
   :param using_locks: If True, the dictionary will be locked when it is being read or written to. This is useful if you are using multiple processes to access the dictionary.
   :param dump_kwargs: Any keyword arguments to pass to the dump method of the format.
"""
```

A nice tip is to do partial application of the function arguments. For instance if you only want to read toml files and always use locks you could use `partial` from functools to do this:

```python
from functools import partial
import toml

persistentdict = partial(persistentdict, format=toml, using_locks=True)
```
