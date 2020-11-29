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

Example local file, e.g. data-quotes-2020-01-01T10-00-00.parquet::

  FEEDS = {
  'data-%(name)s-%(time)s.parquet': {
          'format': 'parquet',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
             'compression': 'GZIP',
             'times': 'int64',
             'hasnulls': True,
             'convertallstrings': False,
             'writeindex': False,
             'objectencoding': 'infer',
             'rowgroupoffset': 50000000,
             'items_rowgroup': 10000
          },
      }
  }

Example s3 file, e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.parquet::

  FEEDS = {
  's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.parquet': {
          'format': 'parquet',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
             'compression': 'GZIP',
             'times': 'int64',
             'hasnulls': True,
             'convertallstrings': False,
             'writeindex': False,
             'objectencoding': 'infer',
             'rowgroupoffset': 50000000,
             'items_rowgroup': 10000
          },
      }
  }
There are more storage backend, e.g. Google Cloud. See the documentation linked above.

Finally, you can define in the FEEDS settings various options in 'item_export_kwargs'

.. list-table:: Options for Parquet export
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - 'compression'
     - 'compression' : 'GZIP'
     - Compression to be used in Parquet: 'UNCOMPRESSED', 'GZIP', 'SNAPPY', 'LZO', 'BROTLI','LZ4','ZSTD'. Instead of a string, you can also specify a dict containing compression options (see `here <https://fastparquet.readthedocs.io/en/latest/api.html#fastparquet.write>`_)
   * - 'times'
     - 'times' : 'int64'
     - type for times 'int64' or 'int96', older spark versions are int96 only
   * - 'convertallstrings'
     - 'convertallstrings' : False
     - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
   * - 'hasnulls'
     - 'hasnulls' : True
     - can contain nulls
   * - 'writeindex'
     - 'writeindex' : False
     - write index as extra column
   * - 'objectencoding'
     - 'objectencoding' : 'infer'
     - As of version 0.4.0. Data type of columns. infer is a special type and means that fastparquet tries to detect it automatically. Can be str or dictionary in the format {col: type}, and type can be infer|bytes|utf8|json|bson|bool|int|int32|float|decimal, where bytes is assumed if not specified (i.e., no conversion) (see `here <https://fastparquet.readthedocs.io/en/latest/api.html#fastparquet.write>`_)
   * - 'rowgroupoffset'
     - 'rowgroupoffset':50000000
     - offset row groups
   * - 'items_rowgroup'
     - 'items_rowgroup' : 10000
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
     - `python-lzo <https://pypi.org/project/python-lzo/>`_
   * - 'BROTLI'
     - BROTLI compression (note: scrapy requires brotlipy, but fastparquet brotli)
     - `brotli <https://pypi.org/project/brotli/>`_
   * - 'ZSTD'
     - Zstandard compression
     - `zstandard <https://pypi.org/project/zstandard/>`_
   * - 'LZ4'
     - LZ4 compression
     - `lz4 <https://pypi.org/project/lz4/>`_
