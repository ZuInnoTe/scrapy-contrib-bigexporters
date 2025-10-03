# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2025-10-03
* Added: Support for [Apache Iceberg](https://iceberg.apache.org/). Note: Iceberg is an open table format and not a file format. It has a lot of different configuration options. Thus, it works a bit differently under Scrapy
* Changed: Minimal Python version: 3.12
* Changed: Minimal dependency versions: Scrapy: 2.13.3, fastavro 1.12.0, pyiceberg 0.10.0, fastparquet 2024.11.0, pyorc 0.10.0
* Changed: Update minimal build dependencies: coverage >= 7.10, tox >=4.30.0, pytest >= 8.4.0, sphinx >= 8.2.0, black >= 25.9.0, prospector >= 1.17.0, pylint >=3.3.0, bandit>= 1.8.0, pycodestyle 

## [0.5.0] - 2024-11-16
* Added: Code formatting using [Black](https://black.readthedocs.io/en/stable/)
* Added: Added [PyPi Trusted Publisher](https://docs.pypi.org/trusted-publishers/) with a dedicated Github action workflow (publish_pypi) in dedicated Github environment
* Changed: Minimal Python version: 3.11
* Changed: Minimal dependency versions: Scrapy 2.11, fastavro 1.9, fastparquet 2024.02, pandas 2.2, pyorc 0.9

## [0.4.0] - 2022-06-25
* Added: Migrate to Pandas concat instead of append due to deprecation [#4](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/4)
* Added: Add basic Github Actions workflow [#5](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/5)
* Added: Add support for pyproject.toml [#6](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/6)
* Added: Add a proper changelog based on https://keepachangelog.com/
* Added: Support for Parquet reader to define a custom schema as an alternative to inferring it


## [0.3.0] (and predecessors) - 2020-11-01
* Added: Initial version with support for parquet, orc and avro export