# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
* Added: Migrate to Pandas concat instead of append due to depreciation [#4](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/4)
* Added: Add basic Github Actions workflow [#5](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/5)
* Added: Add support for pyproject.toml [#6](https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/issues/6)
* Added: Add a proper changelog based on https://keepachangelog.com/
* Added: Support for Parquet reader to define a custom schema as an alternative to inferring it


## [0.3.0] (and predecessors) - 2020-11-01
* Added: Initial version with support for parquet, orc and avro export