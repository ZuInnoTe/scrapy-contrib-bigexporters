======
Export
======

We describe here how to use the Avro exporter with Scrapy.

`Avro <https://avro.apache.org/>`_ is a file format common in Big Data platforms for exchanging data in a structured way.

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_avro>`_


General Guidelines
==================

You need at least the library `fastavro <https://pypi.org/project/fastavro/>`_ to enable the Avro export. You may need additional libraries for special types of compression (see below).

Please look carefully at the options below.

You need in any case define an `Avro schema <https://fastavro.readthedocs.io/en/latest/>`_. Field names in your Avro schema should match the field names that you have defined in your Scrapy scraper project. Carefully look at the types and that your scraper always provides the correct type. Especially in case the data cannot be found on the web page or is not in the expected format (e.g. numbers contain text on the website)


Configuration
=============
You need to configure in your Scrapy project in settings.py the following exporter::

  FEED_EXPORTERS={'avro': 'zuinnote.scrapy.contrib.bigexporters.AvroItemExporter'} # register additional format

Then you need to configure `FEEDS <https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS>`_ in settings.py to define output format and file name.

Local file (e.g. "data-quotes-2020-01-01T10-00-00.avro") with a schema "Author, text, tags"::

  FEEDS = {
        'data-%(name)s-%(time)s.avro': {
            'format':'avro',
            'encoding':'utf8',
            'store_empty': False,
            'item_export_kwargs': {
                 'compression': 'deflate',
                 'compressionlevel': None,
                 'metadata': None,
                 'syncinterval': 16000,
                 'recordcache': 10000,
                 'syncmarker': None,
                 'convertallstrings': False,
                 'validator': None,
                 'avroschema': {
                     'doc': 'Some quotes',
                     'name': 'quotes',
                     'type': 'record',
                     'fields': [
                         {'name': 'text', 'type': 'string'},
                         {'name': 'author', 'type': {
                             'type':'array',
                             'items':'string',
                             'default':[]
                             }
                         },
                         {'name': 'tags', 'type': {
                             'type':'array',
                             'items':'string',
                             'default':[]
                             }
                         },
                     ]
                 }
              }
        }
      }
S3 file (e.g "s3://mybucket/data-quotes-2020-01-01T10-00-00.avro") with a schema "Author, text, tags"::

     FEEDS = {
      's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.avro': {
          'format':'avro',
          'encoding':'utf8',
          'store_empty': False,
          'item_export_kwargs': {
               'compression': 'deflate',
               'compressionlevel': None,
               'metadata': None,
               'syncinterval': 16000,
               'recordcache': 10000,
               'syncmarker': None,
               'convertallstrings': False,
               'validator': None,
               'avroschema': {
                   'doc': 'Some quotes',
                   'name': 'quotes',
                   'type': 'record',
                   'fields': [
                       {'name': 'text', 'type': 'string'},
                       {'name': 'author', 'type': {
                           'type':'array',
                           'items':'string',
                           'default':[]
                           }
                       },
                       {'name': 'tags', 'type': {
                           'type':'array',
                           'items':'string',
                           'default':[]
                           }
                       },
                   ]
               }
            }
      }
    }


There are more storage backend, e.g. Google Cloud. See the documentation linked above.

Finally, you can define in the FEEDS settings various options in 'item_export_kwargs' (and you need to at least define the AvroSchema)

.. list-table:: Options for Avro export
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - 'compression'
     - 'compression' : 'deflate'
     - Compression to be used in Avro: 'null', 'deflate', 'bzip2', 'snappy', 'zstandard', 'lz4', 'xz'
   * - 'compressionlevel'
     - 'compressionlevel' = None
     - Compression level to be used in Avro: can be an integer if supported by codec
   * - 'metadata'
     - 'metadata' : None
     - Avro metadata (dict)
   * - 'syncinterval'
     - 'syncinterval' : 16000
     - sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
   * - 'recordcache'
     - 'recordcache' : 10000
     - how many records should be written at once, the higher the better the compression, but the more memory is needed
   * - 'syncmarker'
     - 'syncmarker' : None
     - bytes, if None then a random byte string is used
   * - 'convertallstrings'
     - 'convertallstrings' : False
     - convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
   * - 'avroschema'
     - 'avroschema' : None
     - Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also `fastavro write <https://fastavro.readthedocs.io/en/latest/writer.html>`_
   * - 'validator'
     - 'validator' : None
     - use fast avro validator when writing, can be None, True (fastavro.validation.validate is used) or a custom function


Additional libraries
====================

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
     - `backports.lzma <https://pypi.org/project/backports.lzma/>`_
