======
Export
======

We describe here how to use the Iceberg exporter with Scrapy.

`Iceberg <https://iceberg.apache.org/>`_ is an open table format common in Big Data platforms for analysing data in a structured way.

Example
=======
You can find an example on how to use it in a Scrapy project `here <../examples/quotes_iceberg>`_


General Guidelines
==================

Please look carefully at the options below.

You need at least the library `pyiceberg <https://pypi.org/project/pyiceberg/>`_ and `pyarrow <https://pypi.org/project/pyarrow/>`_ to enable the Iceberg export. Example::
  pip install pyiceberg[sql-sqlite,s3fs] pyarrow


You may need additional libraries for supporting different catalogs, filesystems and compression (see below).

Note: Iceberg supports connecting multiple different technologies (e.g. databases, object store, file systems etc.) as it is an open table format. Thus, we do not use the export file provided by Scrapy to write the data, but this is configured directly in iceberg. 
We only write in the final file a JSON object indicating the number of items written. The real data is written using pyiceberg to whatever catalog/namespace/table you configured.

Configuration
=============
You need to configure in your Scrapy project in settings.py the following exporter::

  FEED_EXPORTERS={'iceberg': 'zuinnote.scrapy.contrib.bigexporters.IcebergItemExporter'} # register additional format

Then you need to configure `FEEDS <https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS>`_ in settings.py to define output format and file name.
The file you specify as filename only stores how many items have been scraped. The scrapped data will be stored in the Iceberg table within the Iceberg catalog that you specified.

Example local file, e.g. result-quotes-2020-01-01T10-00-00.json::

  FEEDS = {
  'result-%(name)s-%(time)s.json': {
          'format': 'iceberg',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
             'hasnulls': True,
             'convertallstrings': False,
             'no_items_batch': 10000,
             'iceberg_catalog': {
               'default': {
                    'type': 'sql',
                    'uri': 'sqlite:///./warehouse/pyiceberg_catalog.db',
                    'warehouse': 'file:///./warehouse'
               }
             },
              'iceberg_namespace': {
                    'name': 'mynamespace',
                    'create_if_not_exists': True,
                    'properties': {}
              }
              'iceberg_table': {
                    'name': 'mynamespace.scraping_data',
                    'create_if_not_exists': True,
                    'properties': {
                        'write.parquet.compression-codec': 'zstd',
                        'write.parquet.compression-level': 3
                    }
              }
      }
  }


The file you specify as filename only stores how many items have been scraped. 
The scrapped data will be stored in the Iceberg table within the Iceberg catalog that you specified. This Iceberg catalog and table is in the previous example in the local folder ./warehouse


Example s3 file, e.g. s3://mybucket/result-quotes-2020-01-01T10-00-00.json::

  FEEDS = {
  's3://aws_key:aws_secret@mybucket/result-%(name)s-%(time)s.json': {
          'format': 'parquet',
          'encoding': 'utf8',
          'store_empty': False,
          'item_export_kwargs': {
             'hasnulls': True,
             'convertallstrings': False,
             'no_items_batch': 10000,
             'iceberg_catalog': {
               'default': {
                    'type': 'sql',
                    'uri': 'sqlite:///./warehouse/pyiceberg_catalog.db',
                    'warehouse': 'file:///./warehouse'
               }
             },
              'iceberg_namespace': {
                    'name': 'mynamespace',
                    'create_if_not_exists': True,
                    'properties': {}
              }
              'iceberg_table': {
                    'name': 'mynamespace.scraping_data',
                    'create_if_not_exists': True,
                    'properties': {
                        'write.parquet.compression-codec': 'zstd',
                        'write.parquet.compression-level': 3
                    }
              }
          },
      }
  }
There are more storage backends, e.g. Google Cloud. See the documentation linked above. Note: The storage backends supported by Scrapy may differ from the ones supported by Iceberg.

The file you specify as filename only stores how many items have been scraped. 
The scrapped data will be stored in the Iceberg table within the Iceberg catalog that you specified. This Iceberg catalog and table can be on S3, but can also be somewhere completely different.


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
   * - 'hasnulls'
     - 'hasnulls' : True
     - can contain nulls
   * - 'no_items_batch'
     - 'no_items_batch' : 10000
     - How many items should be included in each append call to an Iceberg table. The more you include the better is the performance of the table. Depending on how you configure the table (merge-on-read vs copy-on-write), you need to take into account certain maintenance jobs. If you use copy-on-write then writing is slower as during writes data files are merged. If you use merge-on-read then writing is faster, but you should regularly schedule `maintenance jobs  <https://iceberg.apache.org/docs/nightly/spark-procedures/#named-arguments>`_, such as rewrite_data_files, rewrite_manifests, remove_orphan_files
   * - 'iceberg_catalog'
     - 'iceberg_catalog': {}
     - Configuration of iceberg catalog. Note: This configuration can be complex and has many supported variables (see `here  <https://py.iceberg.apache.org/configuration/>`_). **You need here to configure the catalog, table, data location etc.**
   * - 'iceberg_table'
     - 'iceberg_table': {
                    'name': 'default.scraping_data',
                    'create_if_not_exists': True,
                    'properties': {}
                }
     - Configuration of the table. You can configure the table name in the catalog ('name') and the option 'create_if_not_exists', which if set to True, will create the table in the catalog if it does not exist. Otherwise it will reuse the existing table. Additionally you can specify the `table properties <https://py.iceberg.apache.org/configuration/#tables>`_ in case the table is created using the option 'properties', which expects a Python dictionary. Note: If you require to specify a partition_spec or sort_order then we recommend to create the table outside of your Python script directly in the catalog once beforehand.
   * - 'iceberg_namespace'
     - 'iceberg_namespace': {
                    'name': 'default',
                    'create_if_not_exists': True,
                    'properties': {}
                }
     - Configuration of the namespace. You can configure the namespace in the catalog ('name') and the option 'create_if_not_exists', which if set to True, will create the namespace in the catalog if it does not exist. Otherwise it will reuse the existing namespace. Additionally you can specify the `namespace properties <https://py.iceberg.apache.org/configuration/#tables>`_ in case the namespace is created using the option 'properties', which expects a Python dictionary.

   
Additional libraries
====================

Depending on what catalog, FileIO etc. you need you will need to install pyiceberg with different dependencies. See `pyiceberg installation <https://py.iceberg.apache.org/#installation>`_

