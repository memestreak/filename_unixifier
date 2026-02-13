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


class FilenameUnixifier:
  """Performs file name updates to be idiomatic to UNIX file conventions."""

  def __init__(self, noop: bool):
    self.noop = noop

  @staticmethod
  def denoise_string(input_string: str):
    """Returns the input string with common garbage removed or mitigated."""

    ret_val = input_string.lower()
    ret_val = re.sub(' ', '_', ret_val)

    # Polish
    ret_val = re.sub('&', '_and_', ret_val)

    # Clobber or replace any weird characters.
    ret_val = re.sub(r'["\'’`~]', '', ret_val)
    ret_val = re.sub(r'[^\w\._-]', '_', ret_val)

    # This can happen around track numbers.
    ret_val = re.sub(r'_-', '-', ret_val)
    ret_val = re.sub(r'-_', '-', ret_val)
    ret_val = re.sub(r'\._', '_', ret_val)

    # Removing dupes and underscores from beginning and end.
    ret_val = re.sub(r'_+', '_', ret_val)
    ret_val = re.sub(r'^[_-]?', '', ret_val)
    ret_val = re.sub(r'_$', '', ret_val)

    return ret_val

  @staticmethod
  def generate_new_name(orig_name: str):
    """Returns a computed name based on the specified original."""

    # Separate the [optional] suffix to make things simpler.
    path: pathlib.Path = pathlib.Path(orig_name)
    suffix: str = FilenameUnixifier.denoise_string(path.suffix)

    # Stem is the base filename without extension.
    stem: str = path.stem

    # Extract a possible numeric prefix for cleanup.
    matches = re.match(r'(([0-9]+)[\W]+)?(.*)', stem)
    if not matches:
      print('Unexpected failure to parse filename stem:', stem)
      return orig_name

    numeric_prefix_string = matches.group(2) if matches.group(2) else ''
    new_stem = matches.group(3)
    new_stem = FilenameUnixifier.denoise_string(new_stem)

    if numeric_prefix_string:
      new_stem = f'{numeric_prefix_string}-{new_stem}'

    return new_stem + suffix

  def __do_rename(self,
                  orig_path: pathlib.Path,
                  new_path: pathlib.Path):

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
    file_to_process: pathlib.Path = pathlib.Path(filename)
    parent: pathlib.Path = file_to_process.parent
    orig_name: str = file_to_process.name
    new_name: str = self.generate_new_name(orig_name)
    new_path: pathlib.Path = parent.joinpath(new_name)

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
    IPython.embed()  # type: ignore[no-untyped-call]
    return

  for filename in args.filename:
    renamer.rename_file(filename)


if __name__ == '__main__':
  main()
