# 🌟 **PyPI-Ready Django App Template**

```
myapp_template/
│
├─ myapp/                      # App code
│   ├─ __init__.py
│   ├─ __version__.py          # Version file
│   ├─ admin.py
│   ├─ apps.py
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ forms.py
│   ├─ templatetags/
│   │   ├─ __init__.py
│   │   └─ myapp_tags.py
│   ├─ templates/
│   │   └─ myapp/base.html
│   └─ static/
│       └─ myapp/style.css
│
├─ tests/
│   ├─ __init__.py
│   ├─ test_models.py
│   ├─ test_views.py
│   └─ test_forms.py
│
├─ .github/workflows/ci.yml   # GitHub Actions CI/CD
├─ setup.py
├─ pyproject.toml             # Modern build system
├─ MANIFEST.in
├─ README.md
├─ LICENSE
├─ .gitignore
└─ tox.ini                    # Optional local testing automation
```

---

## **1. Version File (`__version__.py`)**

```python
__version__ = "0.1.0"
```

`setup.py` will import this:

```python
from myapp.__version__ import __version__
```

---

## **2. setup.py Example**

```python
from setuptools import setup, find_packages
from myapp.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="myapp",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=3.2"],
    author="Your Name",
    author_email="you@example.com",
    description="A reusable Django app template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/myapp",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

---

## **3. pyproject.toml (PEP 517/518)**

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"
```

---

## **4. MANIFEST.in**

```
include README.md LICENSE
recursive-include myapp/templates *
recursive-include myapp/static *
```

---

## **5. GitHub Actions CI/CD (`.github/workflows/ci.yml`)**

```yaml
name: Django App CI/CD

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e .
      - name: Run tests
        run: python manage.py test
  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install build tools
        run: pip install --upgrade build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
          TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: twine upload dist/*
```

> **Note:** Store your PyPI credentials as GitHub Secrets: `PYPI_USERNAME` and `PYPI_PASSWORD`.

---

## **6. Optional Tox Automation (`tox.ini`)**

```ini
[tox]
envlist = py310, py311

[testenv]
deps =
    Django>=3.2
commands =
    python manage.py test
```

* Run `tox` locally to test in multiple Python versions.

---

## **7. Badges in README.md**

```markdown
# MyApp

[![PyPI version](https://badge.fury.io/py/myapp.svg)](https://badge.fury.io/py/myapp)
[![CI](https://github.com/username/myapp/actions/workflows/ci.yml/badge.svg)](https://github.com/username/myapp/actions)
[![Python Version](https://img.shields.io/pypi/pyversions/myapp)](https://pypi.org/project/myapp/)
```

---

## **8. Publishing Steps**

1. Build locally:

```bash
python -m build
```

2. Test installation locally:

```bash
pip install dist/myapp-0.1.0-py3-none-any.whl
```

3. Push to GitHub → triggers CI → runs tests → optionally publishes to PyPI automatically.

---

## ✅ **PyPI-Ready Template Checklist**

* [x] Namespaced templates & static
* [x] setup.py, pyproject.toml, MANIFEST.in
* [x] Version in `__version__.py`
* [x] GitHub Actions CI/CD workflow
* [x] tox.ini for local testing
* [x] README with badges
* [x] LICENSE included
* [x] Tests pass on multiple Python versions
* [x] Build & install tested locally
* [x] Ready to publish to PyPI


