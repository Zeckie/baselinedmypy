"""Test cases for running mypy programs using a Python interpreter.

Each test case type checks a program then runs it using Python. The
output (stdout) of the program is compared to expected output. Type checking
uses full builtins and other stubs.

Note: Currently Python interpreter paths are hard coded.

Note: These test cases are *not* included in the main test suite, as including
      this suite would slow down the main suite too much.
"""

from __future__ import annotations

import os
import os.path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from mypy import api
from mypy.defaults import PYTHON3_VERSION
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal, split_lines

# Path to Python 3 interpreter
python3_path = sys.executable
program_re = re.compile(r"\b_program.py\b")


class PythonEvaluationSuite(DataSuite):
    files = ["pythoneval.test", "pythoneval-asyncio.test"]
    cache_dir = TemporaryDirectory()

    def run_case(self, testcase: DataDrivenTestCase) -> None:
        test_python_evaluation(testcase, os.path.join(self.cache_dir.name, ".mypy_cache"))


def test_python_evaluation(testcase: DataDrivenTestCase, cache_dir: str) -> None:
    """Runs Mypy in a subprocess.

    If this passes without errors, executes the script again with a given Python
    version.
    """
    assert testcase.old_cwd is not None, "test was not properly set up"
    # We must enable site packages to get access to installed stubs.
    # TODO: Enable strict optional for these tests
    mypy_cmdline = [
        "--show-traceback",
        "--no-strict-optional",
        "--no-silence-site-packages",
        "--no-error-summary",
        "--legacy",
    ]
    interpreter = python3_path
    mypy_cmdline.append(f"--python-version={'.'.join(map(str, PYTHON3_VERSION))}")

    m = re.search("# flags: (.*)$", "\n".join(testcase.input), re.MULTILINE)
    if m:
        mypy_cmdline.extend(m.group(1).split())

    # Write the program to a file.
    program = "_" + testcase.name + ".py"
    program_path = os.path.join(test_temp_dir, program)
    mypy_cmdline.append(program_path)
    with open(program_path, "w", encoding="utf8") as file:
        for s in testcase.input:
            file.write(f"{s}\n")
    mypy_cmdline.append(f"--cache-dir={cache_dir}")
    output = []
    # Type check the program.
    out, err, returncode = api.run(mypy_cmdline)
    # split lines, remove newlines, and remove directory of test case
    for line in (out + err).splitlines():
        if line.startswith(test_temp_dir + os.sep):
            output.append(line[len(test_temp_dir + os.sep) :].rstrip("\r\n"))
        else:
            # Normalize paths so that the output is the same on Windows and Linux/macOS.
            line = line.replace(test_temp_dir + os.sep, test_temp_dir + "/")
            output.append(line.rstrip("\r\n"))
    if returncode == 0:
        # Execute the program.
        proc = subprocess.run(
            [interpreter, "-Wignore", program], cwd=test_temp_dir, capture_output=True
        )
        output.extend(split_lines(proc.stdout, proc.stderr))
    # Remove temp file.
    os.remove(program_path)
    for i, line in enumerate(output):
        if os.path.sep + "typeshed" + os.path.sep in line:
            output[i] = line.split(os.path.sep)[-1]
    assert_string_arrays_equal(
        adapt_output(testcase), output, f"Invalid output ({testcase.file}, line {testcase.line})"
    )


def adapt_output(testcase: DataDrivenTestCase) -> list[str]:
    """Translates the generic _program.py into the actual filename."""
    program = "_" + testcase.name + ".py"
    return [program_re.sub(program, line) for line in testcase.output]
