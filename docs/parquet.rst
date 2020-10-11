======
Export
======

We describe here how to use the Parquet exporter with Scrapy.

`Parquet <https://parquet.apache.org/>`_ is a file format common in Big Data platforms for analysing in a structured way.

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_parquet>`_


General Guidelines
==================

Please look carefully at the options below.

You need at least the library `fastparquet <https://pypi.org/project/fastparquet/>`_ to enable the Parquet export. You may need additional libraries for special types of compression (see below).


Configuration
=============
You need to configure in your Scrapy project in settings.py the following exporter::

  FEED_EXPORTERS={'parquet': 'zuinnote.scrapy.contrib.bigexporters.ParquetItemExporter'} # register additional format

Then you need to configure `FEEDS <https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS>`_ in settings.py to define output format and file name.

Local file (e.g. "data-quotes-2020-01-01T10-00-00.parquet")::

  FEEDS = {'data-%(name)s-%(time)s.parquet': {'format':'parquet','encoding':'utf8',store_empty': False}} # store as local file containing spider name and scrape datetime, e.g. data-quotes-2020-01-01T10-00-00.parquet

S3 file (e.g "s3://mybucket/data-quotes-2020-01-01T10-00-00.parquet")::

  FEEDS = {'s3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.parquet': {'format':'parquet','encoding':'utf8',store_empty': False}} # store as s3 file containing spider name and scrape datetime, e.g. e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.parquet


There are more storage backend, e.g. Google Cloud. See the documentation linked above.

Finally, you can fine tune your export by configuring the following options in settings.py:

.. list-table:: Options for Parquet export
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - EXPORTER_PARQUET_COMPRESSION
     - EXPORTER_PARQUET_COMPRESSION = 'GZIP'
     - Compression to be used in Parquet: 'UNCOMPRESSED', 'GZIP', 'SNAPPY', 'LZO', 'BROTLI','LZ4','ZSTD'. Instead of a string, you can also specify a dict containing compression options (see `here <https://fastparquet.readthedocs.io/en/latest/api.html#fastparquet.write>`_)
   * - EXPORTER_PARQUET_TIMES
     - EXPORTER_PARQUET_TIMES = 'int64'
     - type for times 'int64' or 'int96', spark is int96 only
   * - EXPORTER_PARQUET_CONVERTALLSTRINGS
     - EXPORTER_PARQUET_CONVERTALLSTRINGS = False
     - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
   * - EXPORTER_PARQUET_HASNULLS
     - EXPORTER_PARQUET_HASNULLS = True
     - can contain nulls
   * - EXPORTER_PARQUET_WRITEINDEX
     - EXPORTER_PARQUET_WRITEINDEX = False
     - write index as extra column
   * - EXPORTER_PARQUET_ROWGROUPOFFSET
     - EXPORTER_PARQUET_ROWGROUPOFFSET = 50000000
     - offset row groups
   * - EXPORTER_PARQUET_ITEMS_ROWGROUP
     - EXPORTER_PARQUET_ITEMS_ROWGROUP = 10000
     - how many items per rowgroup, should be several thousands, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file


Additional libraries
====================

If you want to use special types of compression then additional libraries may be needed:

.. list-table:: Compression Codecs and required libraries
   :widths: 25 25 50
   :header-rows: 1

   * - Compression Codec
     - Description
     - Additional library
   * - 'UNCOMPRESSED'
     - No compression
     - built-in
   * - 'GZIP'
     -  Gzip compression
     - built-in
   * - 'SNAPPY'
     - Snappy compression
     - `python-snappy <https://pypi.org/project/python-snappy/>`_
   * - 'LZO'
     - LZO compression
     - `lzo <https://pypi.org/project/lzo/>`_
   * - 'BROTLI'
     - BROTLI compression
     - `brotli <https://pypi.org/project/brotli/>`_
   * - 'ZSTD'
     - Zstandard compression
     - `zstandard <https://pypi.org/project/zstandard/>`_
   * - 'LZ4'
     - LZ4 compression
     - `lz4 <https://pypi.org/project/lz4/>`_
