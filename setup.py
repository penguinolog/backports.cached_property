#    Copyright 2020 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Backport of python 3.8 functools.cached_property."""

# External Dependencies
import setuptools

PACKAGE_NAME = "backports.cached_property"

with open("requirements.txt") as f:
    REQUIRED = f.read().splitlines()

with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

KEYWORDS = ["caching", "development"]


setuptools.setup(
    name="backports.cached-property",
    author="Aleksei Stepanov",  # Python Software Foundation (original code author: Nick Coghlan)
    author_email="penguinolog@gmail.com",
    maintainer="Aleksei Stepanov penguinolog@gmail.com",
    url="https://github.com/penguinolog/backports.cached_property",
    license="MIT License",
    description="cached_property() - computed once per instance, cached as attribute",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    python_requires=">=3.6.0",
    install_requires=REQUIRED,
    use_scm_version={"write_to": f"{PACKAGE_NAME.replace('.', '/')}/_version.py"},
)
