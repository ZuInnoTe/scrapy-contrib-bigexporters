===========================
scrapy-contrib-bigexporters
===========================


Overview
========

scrapy-contrib-bigexporters provides additional exporters for the web crawling and scraping framework Scrapy (https://scrapy.org).

The following big data formats are supported:

* Avro: https://avro.apache.org/
* Parquet: https://parquet.apache.org/
* Orc: https://orc.apache.org


Requirements
============

* Python 3.11+
* Scrapy 2.11+
* Works on Linux, Windows, macOS, BSD
* Parquet export requires fastparquet 2024.02+
* Avro export requires fastavro 1.9+
* ORC export requires pyorc 0.9+


Install
=======

The quick way (pip)::

    pip install scrapy-contrib-bigexporters

Alternatively, you can install it from `conda-forge <https://anaconda.org/conda-forge/scrapy-contrib-bigexporters>`_::

    conda install -c conda-forge scrapy-contrib-bigexporters

Depending on which format you want to use you need to install one or more of the following libraries.

Avro::

    pip install fastavro

ORC::

    pip install pyorc

Parquet::

    pip install fastparquet

Additional libraries may be needed for specific compression algorithms. See "Use".

Use
====

Use of the library is simple. Install it with your Scrapy project as described above.You only need to configure the exporter in the Scrapy settings, run your scraper and the data will be exported into your desired format. There is no development needed.

See here for configuring the exporter in settings:

* `Avro <https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/blob/master/docs/avro.rst>`_
* `Parquet <https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/blob/master/docs/parquet.rst>`_
* `ORC <https://github.com/ZuInnoTe/scrapy-contrib-bigexporters/blob/master/docs/orc.rst>`_

Source
======

The source is available at:

* Codeberg (a non-commercial European hosted Git for Open Source): https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters
* Github (an US hosted commercial Git platform): https://github.com/ZuInnoTe/scrapy-contrib-bigexporters
