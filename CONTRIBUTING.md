# Contributing to BaselinedMypy

BaselinedMypy is a fork of [basedmypy](https://github.com/KotlinIsland/basedmypy),
which is a fork of [Mypy](https://github.com/python/mypy).

At this stage, BaselinedMypy is experimental, with a focus on making it easier
to manage baselined errors.

This project isn't currently seeking contributions.
If you spot a bug, or think there is an issue that is specific to baselinedmypy, feel free to report
it on the issues page.

You could also check out the upstream projects:
- [basedmypy](https://github.com/KotlinIsland/basedmypy)
- [Mypy](https://github.com/python/mypy)

The details below are mostly from Mypy, with a few edits to make it more applicable to BaselinedMypy.

## Code of Conduct

Everyone participating in the Mypy community, and in particular in our
issue tracker, pull requests, and chat, is expected to treat
other people with respect and more generally to follow the guidelines
articulated in the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).


## Getting started with development

### Setup


#### (1) Clone the mypy repository and enter into it
```
git clone https://github.com/zeckie/baselinedmypy.git
cd mypy
```

#### (2) Create then activate a virtual environment

For more details, see https://docs.python.org/3/library/venv.html#creating-virtual-environments

##### Windows
```commandline
python -m venv venv
venv\Scripts\activate
```
##### Linux
```commandline
python -m venv venv
source venv/bin/activate
```

#### (3) Install the test requirements and the project
```
pip install -r test-requirements.txt
pip install -e .
hash -r  # This resets shell PATH cache, not necessary on Windows
```

### Running tests

Running the full test suite can take a while, and usually isn't necessary when
preparing a PR. Once you file a PR, the full test suite will run on GitHub.
You'll then be able to see any test failures, and make any necessary changes to
your PR.

However, if you wish to do so, you can run the full test suite
like this:
```
python runtests.py
```

You can also use `tox` to run tests (`tox` handles setting up the test environment for you):
```
tox -e py
```

Some useful commands for running specific tests include:
```
# Use mypy to check mypy's own code
python runtests.py self
# or equivalently:
python -m mypy --config-file mypy_self_check.ini -p mypy

# Run a single test from the test suite
pytest -n0 -k 'test_name'

# Run all test cases in the "test-data/unit/check-dataclasses.test" file
pytest mypy/test/testcheck.py::TypeCheckSuite::check-dataclasses.test

# Run the linter
flake8

# Run formatters
black . && isort .
```

For an in-depth guide on running and writing tests,
see [the README in the test-data directory](test-data/unit/README.md).
