===========================
scrapy-contrib-bigexporters
===========================


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

Depending on which format you want to use you need to install one or more of the following libraries.

Avro::

    pip install fastavro

Parquet::

    pip install fastparquet

Additional libraries may be needed for specific compression algorithms. See "Use".

Use
====

Use of the library is simple. Install it with your Scrapy project as described above.You only need to configure the exporter in the Scrapy settings, run your scraper and the data will be exported into your desired format. There is no development needed.

See here for configuring the exporter in settings:

* `Avro <https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/blob/master/docs/avro.rst>`_
* `Parquet <https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/blob/master/docs/parquet.rst>`_
