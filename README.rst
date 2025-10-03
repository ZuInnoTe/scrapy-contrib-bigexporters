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

The library is published using `pypi trusted publishers <https://docs.pypi.org/trusted-publishers/>`_

Requirements
============

* Python 3.12+
* Scrapy 2.13+
* Works on Linux, Windows, macOS, BSD
* Parquet export requires fastparquet 2024.1+
* Avro export requires fastavro 1.12+
* ORC export requires pyorc 0.10+
* Iceberg export requires pyiceberg 0.10+

Install
=======

The quick way (pip)::

    pip install scrapy-contrib-bigexporters

Alternatively, you can install it from `conda-forge <https://anaconda.org/conda-forge/scrapy-contrib-bigexporters>`_::

    conda install -c conda-forge scrapy-contrib-bigexporters

Depending on which format you want to use you need to install one or more of the following libraries.

Avro::

    pip install fastavro
    
Avro is a file format.

Iceberg::

    pip install pyiceberg pyarrow

Iceberg is an open table format.

Note: Most likely you will need to add specific dependencies so that Iceberg works for you. See `pyiceberg installation <https://py.iceberg.apache.org/#installation>`_

ORC::

    pip install pyorc

ORC is a file format.

Parquet::

    pip install fastparquet

Parquet is a file format.

Additional libraries may be needed for specific compression algorithms. The open table format may require additional libraries also to use different filesystems, catalogs and compression formats. See "Use".

Use
====

Use of the library is simple. Install it with your Scrapy project as described above.You only need to configure the exporter in the Scrapy settings, run your scraper and the data will be exported into your desired format. There is no development needed.

See here for configuring the exporter in settings:

* `Avro <https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters/src/branch/main/docs/avro.rst>`_
* `Iceberg <https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters/src/branch/main/docs/iceberg.rst>`_
* `Parquet <https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters/src/branch/main/docs/parquet.rst>`_
* `ORC <https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters/src/branch/main/docs/orc.rst>`_

Source
======

The source is available at:

* Codeberg (a non-commercial European hosted Git for Open Source): https://codeberg.org/ZuInnoTe/scrapy-contrib-bigexporters
* Github (an US hosted commercial Git platform): https://github.com/ZuInnoTe/scrapy-contrib-bigexporters
