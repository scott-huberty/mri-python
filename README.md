[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/template-python/branch/main/graph/badge.svg?token=KRYRRUXDYY)](https://codecov.io/gh/mscheltienne/template-python)
[![tests](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yaml)
[![doc](https://github.com/mscheltienne/template-python/actions/workflows/doc.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/doc.yaml)

# mri-python

**This package is meant to address my own use cases: e.g. for data analyses and other didactive purposes.**

Tools for interactive as well as scripting-oriented processing of neuroimaging data

## To-dos

This pakcage was generaed form a Template python repository. To bootstrap a project from this template, the
following steps are required:

- [x] Rename the folder `template` to the package name
- [x] Edit `pyproject.toml` and all the `template` entries
- [x] Edit the GitHub workflows in `.github`
- [x] Enable `pre-commit.ci` on https://pre-commit.ci/
- [x] Edit `README.md`
- [x] Edit `MANIFEST.in`
- [x] Edit the package import in `tools/stubgen.py`
- [x] Remove the conda-forge recipe from the ignored files in ``.yamllint.yaml``

The package can then be installed in a given environment with
`pip install -e .` (assuming the current working directory is the root of the
repository).

## Documentation build

If the documentation build is preserved, the following steps are required:

On the `main` branch:
- [x] Edit the project links in `doc\links.inc`
- [x] Edit the landing page `index.rst`
- [x] Edit the sphinx configuration `doc/conf.py`
- [x] Edit the API pages
    - [x] In `doc\api\index.rst`, edit the package name
    - [x] In `doc\api\logging.rst`, edit the current module
- [x] Edit the logging tutorial to replace `from template import` with the correct package name

On the `gh-pages` branch:
- [ ] Edit the links in the landing page `index.html`
