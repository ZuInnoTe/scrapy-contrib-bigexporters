# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]



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