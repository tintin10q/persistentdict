# persistentdict

Persistent dict is a context manager that loads and stores a dict in a file automatically. Inspired by my
[python_json_database_manager](https://github.com/tintin10q/python_json_database_manager) repo. This is essentially a simpler version of that.

## Usage

```python
from persistentdict import persistentdict

with persistentdict("test") as d:
    if "test" not in d:
        d["test"] = "test"
        print("Added 'test' key!")
    else:
        print("'Test' is already there!")

# The second time you run this you will get `'Test' is already there!`

"""
A dictionary that persists to a file on disk.
   :param filename: The file to save the dictionary to.
   :param format=json: The format to save the dictionary in. Should be a class that has a dump and load method and __name__.
   :param using_locks: If True, the dictionary will be locked when it is being read or written to.
                       This is useful if you are using multiple processes to access the dictionary.
   :param dump_kwargs: Any keyword arguments to pass to the dump method of the format.
"""
```

> [!TIP]
> Do partial application of the function arguments. If you only want to read toml files and always use locks you could use `partial` from functools to do this:
>
> ```python
> from persistentdict import persistentdict
> from functools import partial
> import toml
> 
> persistentdict = partial(persistentdict, format=toml, using_locks=True)
> ```

> [!Note]
> For proper [toml](https://toml.io/) integration, you need to install the [toml python package](https://pypi.org/project/toml/).
> The standard library [tomllib](https://docs.python.org/3/library/tomllib.html) module (added in 3.11) is not enough as it can
only load toml files but not create them.


## Storage format

The persistantdict works with anything that implements my `Format` abstract base class. 
That means any object with a `dump` and `load` method and a `__name__` attribute will work as a format.

# Installation

```shell
wget https://github.com/tintin10q/persistentdict/blob/production/persistentdict.py
```
