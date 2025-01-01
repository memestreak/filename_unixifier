#!/usr/bin/env python3

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
      ("01: Song Name.FLAC",               "01-song_name.flac"),
      ("12. Get Back - The Beatles.flac",  "12-get_back-the_beatles.flac"),
      ("03. Some Song (2021 remix).flac",  "03-some_song_2021_remix.flac"),
    ]

    for pair in should_be_equal_tuples:
      input_string = pair[0]
      expected_output = pair[1]
      self.assertEqual(
        self.renamer.generate_new_name(input_string), expected_output)


if __name__ == '__main__':
  unittest.main()


