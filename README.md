Pannote
=======

Installation
------------

```
$ brew install xapian --with-python
$ pip install pannote
```

Usage
-----

Given a directory of text files, pannote will go and index those files using
xapian.  It uses an English stemmer.  Then you give it a term and it will find
all matching files.  Each time it runs, it reindexes everything and deletes the
database.

```
$ pannote --help

Usage: pannote [OPTIONS] DIRECTORY TERM

  A simple program that indexes a directory of text files and allows you to
  search it

Options:
  -0, --print0  separate matches with a null byte in output
  --help        Show this message and exit.
```

Pannote works really well with Facebook's [PathPicker][1].


```
$ pannote /path/to/notes "isomorphic" | fpp
```

[1]: https://github.com/facebook/pathpicker/

License
-------

GPLv3
