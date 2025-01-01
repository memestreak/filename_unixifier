#!/usr/bin/env python3
#
# Updates the names of files to be UNIX idiomatic. E.g., no spaces, etc.
# We can [and have] done this with a shell script, but it gets unwieldy,
# especially with multiple files.
#
# Usage: filename_unixifier.py [--noop] filename [filename] ...

import IPython
import argparse
import os
import pathlib
import re
import sys


class FilenameUnixifier:
  """Performs file name updates to be idiomatic to UNIX file conventions."""

  def __init__(self, noop: bool):
    self.noop = noop

  @staticmethod
  def generate_new_name(orig_name: str):
    """Returns a computed name based on the specified original."""

    # Separate the [optional] suffix to make things simpler.
    path: pathlib.PosixPath = pathlib.Path(orig_name)
    suffix: str = path.suffix.lower()

    # Stem is the base filename without extension.
    stem: str = path.stem

    # Extract a possible numeric prefix for cleanup.
    matches = re.match(r'(([0-9]+)[\W]*)?(.*)', stem)
    numeric_prefix_string = matches.group(2) if matches.group(2) else ''
    new_stem = matches.group(3)

    new_stem = new_stem.lower()
    new_stem = re.sub(' ', '_', new_stem)

    # Polish
    new_stem = re.sub('&', '_and_', new_stem)

    # Clobber or replace any weird characters.
    new_stem = re.sub(r'["\'’`~]', '', new_stem)
    new_stem = re.sub(r'[^\w\._-]', '_', new_stem)

    # This can happen around track numbers.
    new_stem = re.sub(r'_-', '-', new_stem)
    new_stem = re.sub(r'-_', '-', new_stem)
    new_stem = re.sub(r'\._', '_', new_stem)

    # Removing dupes and underscores from beginning and end.
    new_stem = re.sub(r'_+', '_', new_stem)
    new_stem = re.sub(r'^[_-]?', '', new_stem)
    new_stem = re.sub(r'_$', '', new_stem)

    if numeric_prefix_string:
      new_stem = f'{numeric_prefix_string}-{new_stem}'

    return new_stem + suffix

  def __do_rename(self,
                  orig_path: pathlib.PosixPath,
                  new_path: pathlib.PosixPath):

    print(f'"{orig_path}" --> "{new_path}": ', end='')

    if not orig_path.exists():
      print('Error: Source file does not exist ❌')
      return

    if orig_path == new_path:
      print('INFO: skipped ✅')
      return

    if self.noop:
      print('NOOP ✅')
      return

    os.rename(orig_path, new_path)
    print('✅')

  def rename_file(self, filename: str):
    file_to_process: pathlib.PosixPath = pathlib.Path(filename)
    parent: pathlib.PosixPath = file_to_process.parent
    orig_name: str = file_to_process.name
    new_name: str = self.generate_new_name(orig_name)
    new_path: pathlib.PosixPath = parent.joinpath(new_name)

    self.__do_rename(file_to_process, new_path)


def main():
  parser = argparse.ArgumentParser(prog='filename_unixifier.py')

  parser.add_argument(
    '--noop',
    '-n',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='If specified, do not make any file writes (No Operation).')

  parser.add_argument(
    '--ipython',
    '-i',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='Just drop in to an IPython REPL for debugging.')

  parser.add_argument(
    'filename',
    nargs='*',
    type=str,
    default=None,
    help='The file to rename')

  args = parser.parse_args()
  renamer = FilenameUnixifier(noop=args.noop)

  if args.ipython:
    IPython.embed()
    return

  for filename in args.filename:
    renamer.rename_file(filename)


if __name__ == '__main__':
  main()
