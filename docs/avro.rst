======
Export
======

We describe here how to use the avro exporter with Scrapy

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_avro>`_

Additional libraries
====================
You need at least the library `fastavro <https://pypi.org/project/fastavro/>`_ to enable the Avro export.

If you want to use special types of compression then additional libraries may be needed:

.. list-table:: Compression Codecs and required libraries
   :widths: 25 25 50
   :header-rows: 1

   * - Compression Codec
     - Description
     - Additional library
   * - 'null'
     - No compression
     - built-in
   * - 'deflate'
     -  Gzip compression
     - built-in
   * - 'bzip2'
     -  Bzip2 compression
     - built-in
   * - 'snappy'
     - Snappy compression
     - `python-snappy <https://pypi.org/project/python-snappy/>`_
   * - 'zstandard'
     - Zstandard compression
     - `zstandard <https://pypi.org/project/zstandard/>`_
   * - 'lz4'
     - LZ4 compression
     - `lz4 <https://pypi.org/project/lz4/>`_
   * - 'xz'
     - XZ compression
     - `backpots.lzma <https://pypi.org/project/backports.lzma/>`_

Configuration
=============
You need to configure in your Scrapy project in settings.py the following exporter::

  FEED_EXPORTERS={'avro': 'zuinnote.scrapy.contrib.bigexporters.AvroItemExporter'} # register additional format

Then you need to configure `FEEDS <https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS>`_ in settings.py to define output format and file name.

Local file (e.g. "data-quotes-2020-01-01T10-00-00.avro")::

  FEEDS = {'data-%(name)s-%(time)s.avro': {'format':'avro','encoding':'utf8',store_empty': False}} # store as local file containing spider name and scrape datetime, e.g. data-quotes-2020-01-01T10-00-00.avro

S3 file (e.g "s3://mybucket/data-quotes-2020-01-01T10-00-00.avro")::

  FEEDS = {'s3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.avro': {'format':'avro','encoding':'utf8',store_empty': False}} # store as s3 file containing spider name and scrape datetime, e.g. e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.avro


There are more storage backend, e.g. Google Cloud. See the documentation linked above.

Finally, you can fine tune your export by configuring the following options in settings.py:

.. list-table:: Compression Codecs and required libraries
   :widths: 25 25 50
   :header-rows: 1

* - Option
  - Default
  - Description
* - EXPORTER_AVRO_COMPRESSION
  - EXPORTER_AVRO_COMPRESSION = 'deflate'
  - Compression to be used in Avro: 'null', 'deflate', 'bzip2', 'snappy', 'zstandard', 'lz4', 'xz'
* - EXPORTER_AVRO_COMPRESSIONLEVEL
  - EXPORTER_AVRO_COMPRESSIONLEVEL = None
  - Compression level to be used in Avro: can be an integer if supported by codec
* - EXPORTER_AVRO_METADATA
  - EXPORTER_AVRO_METADATA = None
  - Avro metadata (dict)
* - EXPORTER_AVRO_SYNCINTERVAL
  - EXPORTER_AVRO_SYNCINTERVAL = 16000
  - sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
* - EXPORTER_AVRO_RECORDCACHE
  - EXPORTER_AVRO_RECORDCACHE = 10000
  - how many records should be written at once, the higher the better the compression, but the more memory is needed
* - EXPORTER_AVRO_SYNCMARKER
  - EXPORTER_AVRO_SYNCMARKER = None
  - bytes, if None then a random byte string is used
* - EXPORTER_AVRO_CONVERTALLSTRINGS
  - EXPORTER_AVRO_CONVERTALLSTRINGS = False
  - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
* - EXPORTER_AVRO_SCHEMASTRING
  - EXPORTER_AVRO_SCHEMASTRING = None
  - Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also `fastavro write <https://fastavro.readthedocs.io/en/latest/writer.html>`_
* - EXPORTER_AVRO_VALIDATOR
  - EXPORTER_AVRO_VALIDATOR = None
  - use fast avro validator when writing, can be None, True (fastavro.validation.validate or a function)
