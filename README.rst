======
scrapy-contrib-bigexporters
======


Overview
========

scrapy-contrib-bigexporters provides additional exporters for the web crawling and scraping framework Scrapy (https://scrapy.org).

The following big data formats are supported:
* Parquet: https://parquet.apache.org/
* Avro: https://avro.apache.org/


Requirements
============

* Python 3.6+
* Scrapy 2.1+
* Works on Linux, Windows, macOS, BSD
* Parquet export requires fastparquet 0.4.1+
* Avro export requires fastavro 1.0.0.post1+


Install
=======

The quick way::

    pip install scrapy-contrib-bigexporters
