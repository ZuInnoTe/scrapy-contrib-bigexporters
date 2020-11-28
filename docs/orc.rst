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

You need at least the library `pyorc <https://pypi.org/project/pyorc/>`_ to enable the Orc export. You may need additional libraries for special types of compression (see below).

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
             'compression': pyorc.CompressionKind.ZLIB,
             'compressionstrategy': pyorc.CompressionStrategy.SPEED,
             'blocksize': 65536,
             'batchsize': 1024,
             'stripesize': 67108864,
             'recordcache': 10000,
             'schemastring': "",
             'convertallstrings': False,
             'bloomfiltercolumns': None,
             'bloomfilterfpp': 0.05,
             'converters': None,
             'metadata': None
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
             'compression': pyorc.CompressionKind.ZLIB,
             'compressionstrategy': pyorc.CompressionStrategy.SPEED,
             'blocksize': 65536,
             'batchsize': 1024,
             'stripesize': 67108864,
             'recordcache': 10000,
             'schemastring': "",
             'convertallstrings': False,
             'bloomfiltercolumns': None,
             'bloomfilterfpp': 0.05,
             'converters': None,
             'metadata': None
          },
      }
  }


There are more storage backend, e.g. Google Cloud. See the documentation linked above.

Finally, you can define in the FEEDS settings various options in 'item_export_kwargs' (and you need to at least define the schemastring)

.. list-table:: Options for Orc export
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - 'compression'
     - 'compression' : pyorc.CompressionKind.ZLIB
     - compression to be used in orc, see pyorc.CompressionKind (NONE = 0, ZLIB = 1, SNAPPY = 2, LZO = 3, LZ4 = 4, ZSTD = 5
   * - 'compressionstrategy'
     - 'compressionstrategy' = pyorc.CompressionStrategy.SPEED
     - compression strategy to be used in orc, see pyorc.CompressionStrategy (SPEED = 0, COMPRESSION = 1)
   * - 'blocksize'
     - 'blocksize': 65536
     - block size of an ORC bloc
   * - 'batchsize'
     - 'batchsize': 1024
     - batch size
   * - 'stripesize'
     - 'stripesize': 67108864
     - stripe size
   * - 'recordcache'
     - 'recordcache': 10000
     - how many records should be written at once, the higher the better the compression, but the more memory is needed, potentially also bloom filter performance can be increased with higher values
   * - 'schemastring'
     - 'schemastring': ""
     -  Orc schema string, e.g. "struct<text:string,author:array<string>,tags:array<string>>", Mandatory to specify schema. Please name your fields exactly like you name them in your items. See also https://pyorc.readthedocs.io/en/latest/api.html#pyorc.Struct
   * - 'convertallstrings'
     - 'convertallstrings' : False
     - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
   * - 'bloomfiltercolumns'
     - 'bloomfiltercolumns': None
     - List of columns (column name as string) for which to provide a bloom filter. Bloom filters are suitable for columns containing categorical values (low to medium cardinality). They can increase performance for filtering on those columns significantly. See also https://orc.apache.org/api/orc-core/org/apache/orc/util/BloomFilter.html
   * - 'bloomfilterfpp'
     - 'bloomfilterfpp': 0.05
     - False positives probability for bloom filters
   * - 'converters'
     - 'converters': None
     - Define converters, can be a dictionary, where the keys are pyorc.TypeKind and the values are subclasses of ORCConverter
   * - 'metadata'
     - 'metadata': None
     - metadata to be added to ORC file value is bytes (e.g. (extra="info".encode() will lead to {'extra': b'info'}))


Additional libraries
====================

If you want to use special types of compression then additional libraries may be needed:

.. list-table:: Compression Codecs and required libraries
   :widths: 25 25 50
   :header-rows: 1

   * - Compression Codec
     - Description
     - Additional library
   * - NONE = 0
     - No compression
     - built-in
   * - ZLIB = 1
     -  Gzip compression
     - built-in
   * - SNAPPY = 2
     - Snappy compression
     - `python-snappy <https://pypi.org/project/python-snappy/>`_
   * - LZO = 3
     - LZO compression
     - `python-lzo <https://pypi.org/project/python-lzo/>`_
   * - LZ4 = 4
     - LZ4 compression
     - `lz4 <https://pypi.org/project/lz4/>`_
   * - ZSTD = 5
     - Zstandard compression
     - `zstandard <https://pypi.org/project/zstandard/>`_
