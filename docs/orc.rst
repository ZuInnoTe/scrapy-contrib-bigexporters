======
Export
======

We describe here how to use the Orc exporter with Scrapy.

`Orc <https://orc.apache.org/>`_ is a file format common in Big Data platforms for analysing data in a structured way using columnar approaches.

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_orc>`_


General Guidelines
==================

You need at least the library `pyarrow <https://pypi.org/project/pyarrow/>`_ to enable the Orc export. You can trim down the needed packages by installing `only a subset of pyarrow <https://arrow.apache.org/docs/python/install.html#dependencies>`_
Please look carefully at the options below.

Note: You need to specify a schema


Configuration
=============
You need to configure in your Scrapy project in settings.py the following exporter::

  FEED_EXPORTERS={'orc': 'zuinnote.scrapy.contrib.bigexporters.OrcItemExporter'} # register additional format

Then you need to configure `FEEDS <https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS>`_ in settings.py to define output format and file name.

Example local file, e.g. data-quotes-2020-01-01T10-00-00.orc::

  FEEDS = {
  'data-%(name)s-%(time)s.orc': {
          'format': 'orc',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
            "no_items_batch": 10000,
            "convertallstrings": False,
            # "file_version": "0.12",
            "batch_size": 1024,
            "stripe_size": 64 * 1024 * 1024,
            "compression": "zstd",
            "compression_block_size": 64 * 1024,
            "compression_strategy": "speed",
            "row_index_stride": 10000,
            "padding_tolerance": 0.0,
            "dictionary_key_size_threshold": 0.0,
            "bloom_filter_columns": None,
            "bloom_filter_fpp": 0.05,
          },
      }
  }

Example S3 file, e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.orc::

  FEEDS = {
  's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.orc': {
          'format': 'orc',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
            "no_items_batch": 10000,
            "convertallstrings": False,
            # "file_version": "0.12",
            "batch_size": 1024,
            "stripe_size": 64 * 1024 * 1024,
            "compression": "zstd",
            "compression_block_size": 64 * 1024,
            "compression_strategy": "speed",
            "row_index_stride": 10000,
            "padding_tolerance": 0.0,
            "dictionary_key_size_threshold": 0.0,
            "bloom_filter_columns": None,
            "bloom_filter_fpp": 0.05,
          },
      }
  }


There are more storage backends, e.g. Google Cloud. See the documentation linked above.

Finally, you can define in the FEEDS settings various options in 'item_export_kwargs'.

.. list-table:: Options for Orc export
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
     - how many items to append to the orc file at once, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final orc file
   * - 'schema'
     - 'schema' : None
     - pyarrow schema to be used for Pandas to Pyarrow conversion
   * - 'pyarrow_safe_schema'
     - 'pyarrow_safe_schema' : True
     - safe schema conversion from Pandas (see `here  <https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table.from_pandas>`_)
   * - `pyarrow orc options  <https://arrow.apache.org/docs/python/generated/pyarrow.orc.ORCWriter.html>`_
     - same as for pyarrow ORCWriter except compression which is set to zstd 
     - You can define most of the pyarrow.orc.ORCWriter options. Just set the name of the option to the desired value. For example, "compression": "zstd". Note: Since scrapy-contrib-bigexporter the names have changed and are now the same as for pyarrow.ORCWriter!


   

