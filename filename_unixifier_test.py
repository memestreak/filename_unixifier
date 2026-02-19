#!/usr/bin/env python3

import os
import shutil
import tempfile
import unittest

import filename_unixifier


class TestConversion(unittest.TestCase):
  def setUp(self):
    self.renamer = filename_unixifier.FilenameUnixifier(noop=True)

  def test_suffix_renaming(self):
    self.assertEqual(
      self.renamer.generate_new_name('some_name.JPG'), 'some_name.jpg')

  def test_and_handling(self):
    self.assertEqual(
      self.renamer.generate_new_name('peanut butter & jelly'), 'peanut_butter_and_jelly')

  def test_common_cases(self):
    should_be_equal_tuples = [
      ("01: Song Name.FLAC",                "01-song_name.flac"),
      ("12. Get Back - The Beatles.flac",   "12-get_back-the_beatles.flac"),
      ("03. Some Song (2021 remix).flac",   "03-some_song_2021_remix.flac"),
      ("48k (Fractal, Line 6, Suhr, etc.)", "48k_fractal_line_6_suhr_etc"),
    ]

    for pair in should_be_equal_tuples:
      input_string = pair[0]
      expected_output = pair[1]
      self.assertEqual(
        self.renamer.generate_new_name(input_string), expected_output)


class TestDenoiseString(unittest.TestCase):
  """Tests for FilenameUnixifier.denoise_string() in isolation."""

  def denoise(self, s):
    return filename_unixifier.FilenameUnixifier.denoise_string(s)

  def test_empty_string(self):
    self.assertEqual(self.denoise(''), '')

  def test_lowercase_conversion(self):
    self.assertEqual(self.denoise('HELLO'), 'hello')

  def test_spaces_to_underscores(self):
    self.assertEqual(self.denoise('hello world'), 'hello_world')

  def test_ampersand_to_and(self):
    self.assertEqual(self.denoise('a & b'), 'a_and_b')

  def test_single_quote_removed(self):
    self.assertEqual(self.denoise("it's"), 'its')

  def test_double_quote_removed(self):
    self.assertEqual(self.denoise('"quoted"'), 'quoted')

  def test_backtick_removed(self):
    self.assertEqual(self.denoise('`foo`'), 'foo')

  def test_tilde_removed(self):
    self.assertEqual(self.denoise('~foo~'), 'foo')

  def test_underscore_dash_normalized(self):
    self.assertEqual(self.denoise('foo_-bar'), 'foo-bar')

  def test_dash_underscore_normalized(self):
    self.assertEqual(self.denoise('foo-_bar'), 'foo-bar')

  def test_dot_underscore_normalized(self):
    self.assertEqual(self.denoise('foo._bar'), 'foo_bar')

  def test_duplicate_underscores_collapsed(self):
    self.assertEqual(self.denoise('foo__bar'), 'foo_bar')

  def test_leading_underscore_removed(self):
    self.assertEqual(self.denoise('_foo'), 'foo')

  def test_trailing_underscore_removed(self):
    self.assertEqual(self.denoise('foo_'), 'foo')

  def test_leading_dash_removed(self):
    self.assertEqual(self.denoise('-foo'), 'foo')

  def test_dots_and_dashes_preserved(self):
    self.assertEqual(self.denoise('my-file.name'), 'my-file.name')


class TestGenerateNewNameEdgeCases(unittest.TestCase):
  """Edge cases for generate_new_name() not covered by TestConversion."""

  def setUp(self):
    self.renamer = filename_unixifier.FilenameUnixifier(noop=True)

  def test_no_extension(self):
    self.assertEqual(
      self.renamer.generate_new_name('My File'), 'my_file')

  def test_already_clean_name_unchanged(self):
    self.assertEqual(
      self.renamer.generate_new_name('my_file.txt'), 'my_file.txt')

  def test_numeric_prefix_without_separator_is_not_extracted(self):
    # "48k" starts with digits but is followed by a word char, so no prefix.
    self.assertEqual(
      self.renamer.generate_new_name('48k_sample'), '48k_sample')


class TestRenameFile(unittest.TestCase):
  """Tests for rename_file() / __do_rename() using a real temp directory."""

  def setUp(self):
    self.temp_dir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.temp_dir, ignore_errors=True)

  def _make_file(self, name):
    path = os.path.join(self.temp_dir, name)
    open(path, 'w').close()
    return path

  def test_nonexistent_file_does_not_raise(self):
    renamer = filename_unixifier.FilenameUnixifier(noop=False)
    # Should print an error message but not raise an exception.
    renamer.rename_file(os.path.join(self.temp_dir, 'does_not_exist.txt'))

  def test_noop_does_not_rename(self):
    orig = self._make_file('My File.txt')
    renamer = filename_unixifier.FilenameUnixifier(noop=True)
    renamer.rename_file(orig)
    self.assertTrue(os.path.exists(orig))
    expected = os.path.join(self.temp_dir, 'my_file.txt')
    self.assertFalse(os.path.exists(expected))

  def test_rename_actually_renames(self):
    orig = self._make_file('My File.txt')
    renamer = filename_unixifier.FilenameUnixifier(noop=False)
    renamer.rename_file(orig)
    self.assertFalse(os.path.exists(orig))
    expected = os.path.join(self.temp_dir, 'my_file.txt')
    self.assertTrue(os.path.exists(expected))

  def test_already_clean_name_is_skipped(self):
    orig = self._make_file('my_file.txt')
    renamer = filename_unixifier.FilenameUnixifier(noop=False)
    renamer.rename_file(orig)
    # File should still exist at its original path.
    self.assertTrue(os.path.exists(orig))


if __name__ == '__main__':
  unittest.main()


