#!/usr/bin/env python3
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for check_cmake_includes.py."""

import os
import pathlib
import tempfile
from typing import Iterable, Mapping
import unittest

import check_cmake_includes


class ConfigureFileParserTest(unittest.TestCase):

  def test_init_positional_args(self):
    path = object()

    parser = check_cmake_includes.ConfigureFileParser(path)

    self.assertIs(parser.path, path)

  def test_init_keyword_args(self):
    path = object()

    parser = check_cmake_includes.ConfigureFileParser(path=path)

    self.assertIs(parser.path, path)

  def test_parse_empty_file_returns_empty_defines(self):
    path = create_temp_file(self)
    parser = check_cmake_includes.ConfigureFileParser(path=path)

    parse_result = parser.parse()

    self.assertEqual(parse_result.defines, frozenset())

  def test_parse_file_with_cmakedefines_returns_those_defines(self):
    configure_file_lines = [
      "#cmakedefine SOME_VAR1",
      "#cmakedefine SOME_VAR2 some_value",
      "#cmakedefine   SOME_VAR3 some_value1 some_value2",
    ]
    path = create_temp_file(self, lines=configure_file_lines)
    parser = check_cmake_includes.ConfigureFileParser(path=path)

    parse_result = parser.parse()

    expected_defines = frozenset(["SOME_VAR1", "SOME_VAR2", "SOME_VAR3"])
    self.assertEqual(parse_result.defines, expected_defines)


class CppFileParserTest(unittest.TestCase):

  def test_init_positional_args(self):
    path = object()

    parser = check_cmake_includes.CppFileParser(path)

    self.assertIs(parser.path, path)

  def test_init_keyword_args(self):
    path = object()

    parser = check_cmake_includes.CppFileParser(path=path)

    self.assertIs(parser.path, path)

  def test_parse_empty_file_returns_empty_result(self):
    path = create_temp_file(self)
    parser = check_cmake_includes.CppFileParser(path=path)

    parse_result = parser.parse()

    self.assert_result(
        parse_result,
        includes=[],
        defines_used={},
    )

  def test_parse(self):
    cpp_file_lines = [
      "#include \"a/b/file_1.h\"",
      "#include     \"a/b/file_2.h\"",
      "#InCluDe \"file_3.h\"",
      "#define INTERNAL_DEFINE_1",
      "#define INTERNAL_DEFINE_2 123",
      "#define   INTERNAL_DEFINE_3 abc",
      "#if VAR1",
      "#ifdef VAR2",
      "#ifndef VAR3",
      "#elif VAR4",
      "#else",
      "#endif",
      "#IMadeThisUp VAR_WITH_UNDERSCORES",
      "int main(int argc, char** argv) {",
      "  return 0;"
      "}"
    ]
    path = create_temp_file(self, lines=cpp_file_lines)
    parser = check_cmake_includes.CppFileParser(path=path)

    parse_result = parser.parse()

    self.assert_result(
        parse_result,
        includes=["a/b/file_1.h", "a/b/file_2.h", "file_3.h"],
        defines_used={
          "VAR1": 7,
          "VAR2": 8,
          "VAR3": 9,
          "VAR4": 10,
          "VAR_WITH_UNDERSCORES": 13,
        },
    )

  def assert_result(
      self,
      parse_result: check_cmake_includes.CppFileParserResult,
      includes: Iterable[str],
      defines_used: Mapping[str, int],
  ) -> None:
    with self.subTest("includes"):
      self.assertEqual(parse_result.includes, frozenset(includes))
    with self.subTest("defines_used"):
      self.assertEqual(parse_result.defines_used, defines_used)


class MissingIncludeTest(unittest.TestCase):

  def test_init_positional_args(self):
    define = object()
    include = object()
    line_number = object()

    missing_include = check_cmake_includes.MissingInclude(
        define, include, line_number)

    self.assertIs(missing_include.define, define)
    self.assertIs(missing_include.include, include)
    self.assertIs(missing_include.line_number, line_number)

  def test_init_keyword_args(self):
    define = object()
    include = object()
    line_number = object()

    missing_include = check_cmake_includes.MissingInclude(
        define=define,
        include=include,
        line_number=line_number,
    )

    self.assertIs(missing_include.define, define)
    self.assertIs(missing_include.include, include)
    self.assertIs(missing_include.line_number, line_number)

  def test_eq(self):
    value1 = check_cmake_includes.MissingInclude("define1", "include1", 1)
    value1_clone = check_cmake_includes.MissingInclude("define1", "include1", 1)
    value2 = check_cmake_includes.MissingInclude("defineX", "include1", 1)
    value3 = check_cmake_includes.MissingInclude("define1", "includeX", 1)
    value4 = check_cmake_includes.MissingInclude("define1", "includeX", 2)

    self.assertTrue(value1 == value1_clone)
    self.assertFalse(value1 != value1_clone)
    self.assertTrue(value1 != value2)
    self.assertFalse(value1 == value2)
    self.assertTrue(value1 != value3)
    self.assertFalse(value1 == value3)
    self.assertTrue(value1 != value4)
    self.assertFalse(value1 == value4)
    self.assertTrue(value1 != None)
    self.assertFalse(value1 == None)

  def test_str(self):
    missing_include = check_cmake_includes.MissingInclude("NAME", "FILE", 99)

    str_value = f"{missing_include}"

    self.assertIn("99", str_value)
    self.assertIn("NAME", str_value)
    self.assertIn("FILE", str_value)
    
  def test_repr(self):
    missing_include = check_cmake_includes.MissingInclude("NAME", "FILE", 99)

    repr_value = f"{missing_include!r}"

    expected_repr_value = (f"MissingInclude(define={'NAME'!r}, "
        f"include={'FILE'!r}, line_number={99!r})")
    self.assertEqual(repr_value, expected_repr_value)
    

class RequiredIncludesCheckerTest(unittest.TestCase):

  def test_init_positional_args(self):
    defines = object()

    checker = check_cmake_includes.RequiredIncludesChecker(defines)

    self.assertIs(checker.defines, defines)

  def test_init_keyword_args(self):
    defines = object()

    checker = check_cmake_includes.RequiredIncludesChecker(defines=defines)

    self.assertIs(checker.defines, defines)

  def test_check_file_returns_empty_list_if_defines_is_empty(self):
    lines = ["#if HELLO"]
    path = create_temp_file(self, lines=lines)
    checker = check_cmake_includes.RequiredIncludesChecker(defines={})

    missing_includes = checker.check_file(path)

    self.assertEqual(missing_includes, tuple())

  def test_check_file_returns_empty_list_if_no_missing_includes(self):
    lines = [
        "#include \"file_1.h\"",
        "#include \"a/b/file_2.h\"",
        "#define DEFINED_VAR 1",
        "#if VAR_1",
        "#if  VAR_2",
        "#elif UNSPECIFIED_DEFINE",
    ]
    defines = {
      "VAR_1": "file_1.h",
      "VAR_2": "a/b/file_2.h",
      "UNUSED_VAR": "a/b/unused.h",
    }
    path = create_temp_file(self, lines=lines)
    checker = check_cmake_includes.RequiredIncludesChecker(defines={})

    missing_includes = checker.check_file(path)

    self.assertEqual(missing_includes, tuple())

  def test_check_file_returns_the_missing_define(self):
    lines = [
        "#if   VAR1",
        "#elif VAR2",
        "#elif VAR2 again",
        "#ifndef UNSPECIFIED_DEFINE",
    ]
    defines = {
      "VAR1": "file1.h",
      "VAR2": "file2.h",
    }
    path = create_temp_file(self, lines=lines)
    checker = check_cmake_includes.RequiredIncludesChecker(defines=defines)

    missing_includes = checker.check_file(path)

    expected_missing_includes = (
      check_cmake_includes.MissingInclude(
        define="VAR1", include="file1.h", line_number=1),
      check_cmake_includes.MissingInclude(
        define="VAR2", include="file2.h", line_number=2),
    )
    self.assertCountEqual(missing_includes, expected_missing_includes)


class ConfigBuilderTest(unittest.TestCase):

  def test_empty_config(self):
    config_builder = check_cmake_includes.ConfigBuilder()

    config = config_builder.build()

    self.assertEqual(config.cmake_configure_paths, {})
    self.assertCountEqual(config.files_to_scan, [])

  def test_nonempty_config(self):
    config_builder = check_cmake_includes.ConfigBuilder()
    config_builder.add_cmake_config_path(pathlib.Path("a/b/c.in"), "c.h")
    config_builder.add_cmake_config_path(pathlib.Path("d/e/f.in"), "f.h")
    config_builder.add_file_to_scan(pathlib.Path("src/a/f1.cc"))
    config_builder.add_file_to_scan(pathlib.Path("src/b/f2.cc"))

    config = config_builder.build()

    self.assertEqual(config.cmake_configure_paths, {
      pathlib.Path("a/b/c.in"): "c.h",
      pathlib.Path("d/e/f.in"): "f.h",
    })
    self.assertCountEqual(config.files_to_scan, [
      pathlib.Path("src/a/f1.cc"),
      pathlib.Path("src/b/f2.cc"),
    ])


def create_temp_file(
    test_case: unittest.TestCase,
    lines: Iterable[str] = tuple(),
) -> pathlib.Path:
  (handle, path_str) = tempfile.mkstemp()

  with os.fdopen(handle, "wt", encoding="utf8") as f:
    if lines:
      for line in lines:
        print(line, file=f)

  test_case.addCleanup(os.remove, path_str)
  return pathlib.Path(path_str)


if __name__ == "__main__":
  unittest.main()
