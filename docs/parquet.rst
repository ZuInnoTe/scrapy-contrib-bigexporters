======
Export
======

We describe here how to use the Parquet exporter with Scrapy.

`Parquet <https://parquet.apache.org/>`_ is a file format common in Big Data platforms for analysing data in a structured way.

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_parquet>`_


General Guidelines
==================

Please look carefully at the options below.

You need at least the library `pyarrow <https://pypi.org/project/pyarrow/>`_ to enable the Parquet export. You can trim down the needed packages by installing `only a subset of pyarrow <https://arrow.apache.org/docs/python/install.html#dependencies>`_
Please look carefully at the options below.


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
             'convertallstrings': False,
             'no_items_batch': 10000,
             'compression': 'zstd',
             'compression_level': 3
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
             'convertallstrings': False,
             'no_items_batch': 10000,
             'compression': 'zstd',
             'compression_level': 3
          },
      }
  }


Be aware that you should not use static credentials, such as secret key and access key, for accessing resources, such as S3, but machine identities such as AWS IAM Roles based on short-living tokens.

Note: You can define many more options (see below), e.g. most of pyarrow.ParquetWriter

There are more storage backends, e.g. Google Cloud. See the documentation linked above.

Finally, you can define in the FEEDS settings various options in 'item_export_kwargs'

.. list-table:: Options for Parquet export
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - 'convertallstrings'
     - 'convertallstrings' : False
     - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
   * - 'no_items_batch'
     - 'no_items_batch' : 10000
     - how many items to append to the parquet file at once, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file
   * - 'row_group_size'
     - 'row_group_size' : None
     - Maximum number of rows in each written row group. If None, the row group size will be the minimum of the Table size (in rows) and 1024 * 1024.    
   * - `pyarrow parquet options  <https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetWriter.html>`_
     - same as for pyarrow.parquet.ParquetWriter except compression which is set to zstd 
     - You can define most of the pyarrow.parquet.Parquetwriter options. Just set the name of the option to the desired value. For example, "compression": "zstd". Note: Since scrapy-contrib-bigexporter the names have changed and are now the same as for pyarrow.ParquetWriter!

