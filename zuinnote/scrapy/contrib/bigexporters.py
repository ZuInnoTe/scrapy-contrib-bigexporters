"""
Copyright (c) 2020 ZuInnoTe (Jörn Franke) <zuinnote@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
   Contains various formats for exporting data from the web crawling framework scrapy
"""


"""
Parquet exporter
Write export as parquet file (based on fastparquet - you need to add the latest version as a dependency)
Custom parquet feed exporter
FEED_EXPORTERS={'parquet': 'zuinnote.scrapy.contrib.bigexporters.ParquetItemExporter'} # register additional format
Example local file, e.g. data-quotes-2020-01-01T10-00-00.parquet
FEEDS = {
'data-%(name)s-%(time)s.parquet': {
        'format': 'parquet',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': 'GZIP', # compression to be used in Parquet, UNCOMPRESSED, GZIP, SNAPPY (package: python-snappy), LZO (package: lzo), BROTLI (package: brotli), LZ4 (package: lz4), ZSTD (package: zstandard) note: compression may require additional libraries
           'times': 'int64', # type for times int64 or int96, spark is int96 only
           'hasnulls': True,# can contain nulls
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'writeindex': False, # write index as extra column
           'objectencoding': 'infer', # schema of data
           'rowgroupoffset': 50000000, # offset row groups
           'items_rowgroup': 10000  # how many items per rowgroup, should be several thousands, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file
        },
    }
}

Example s3 file, e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.parquet
FEEDS = {
's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.parquet': {
        'format': 'parquet',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': 'GZIP', # compression to be used in Parquet, UNCOMPRESSED, GZIP, SNAPPY (package: python-snappy), LZO (package: lzo), BROTLI (package: brotli), LZ4 (package: lz4), ZSTD (package: zstandard) note: compression may require additional libraries
           'times': 'int64', # type for times int64 or int96, spark is int96 only
           'hasnulls': True,# can contain nulls
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'writeindex': False, # write index as extra column
           'objectencoding': 'infer', # schema of data
           'rowgroupoffset': 50000000, # offset row groups
           'items_rowgroup': 10000  # how many items per rowgroup, should be several thousands, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file
        },
    }
}

see: https://docs.scrapy.org/en/latest/topics/exporters.html
"""

"""
Avro exporter
Write export as avro file (based on fastavro - you need to add the latest version as a dependency)

Custom avro feed exporter
FEED_EXPORTERS={'avro': 'zuinnote.scrapy.contrib.bigexporters.AvroItemExporter'} # register additional format
Possible options in settings.py and their default settings using FEEDS
Example local file, e.g. data-quotes-2020-01-01T10-00-00.avro
FEEDS = {
'data-%(name)s-%(time)s.avro': {
        'format': 'avro',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': 'deflate',# compression to be used in Avro, null, deflate, bzip2, snappy (package: python-snappy), zstandard(package: zstandard), lz4 (package: lz4) , xz (packahe: backports.lzma) note: compression may require additional libraries
           'compressionlevel': None, # codec specific compression level, can be an integer if supported by codec
           'metadata': None,# metadata (dict)
           'syncinterval': 16000, # sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
           'recordcache': 10000, # how many records should be written at once, the higher the better the compression, but the more memory is needed
           'syncmarker': None, # bytes, if None then a random byte string is used
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'validator': None, # use fast avro validator when writing, can be None, True (fastavro.validation.validate or a function)
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
           } # Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also https://fastavro.readthedocs.io/en/latest/writer.html
        },
    }
}

Example s3 file, e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.avro
FEEDS = {
's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.avro': {
        'format': 'avro',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': 'deflate',# compression to be used in Avro, null, deflate, bzip2, snappy (package: python-snappy), zstandard(package: zstandard), lz4 (package: lz4) , xz (packahe: backports.lzma) note: compression may require additional libraries
           'compressionlevel': None, # codec specific compression level, can be an integer if supported by codec
           'metadata': None,# metadata (dict)
           'syncinterval': 16000, # sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
           'recordcache': 10000, # how many records should be written at once, the higher the better the compression, but the more memory is needed
           'syncmarker': None, # bytes, if None then a random byte string is used
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'validator': None, # use fast avro validator when writing, can be None, True (fastavro.validation.validate or a function)
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
           } # Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also https://fastavro.readthedocs.io/en/latest/writer.html
        },
    }
}

see: https://docs.scrapy.org/en/latest/topics/exporters.html
"""


"""
Orc exporter
Write export as orc file (based on pyorc - you need to add the latest version as a dependency)
Possible options in settings.py and their default settings
Custom orc feed exporter
FEED_EXPORTERS={'orc': 'zuinnote.scrapy.contrib.bigexporters.OrcItemExporter'} # register additional format
Example local file, e.g. data-quotes-2020-01-01T10-00-00.orc

FEEDS = {
'data-%(name)s-%(time)s.orc': {
        'format': 'orc',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': pyorc.CompressionKind.ZLIB, # compression to be used in orc, see pyorc.CompressionKind (None = 0, ZLIB = 1, SNAPPY = 2 (package: python-snappy), LZO = 3 (package: lzo), LZ4 = 4 (package: lz4), ZSTD = 5 (package: zstandard), note: compression may require additional libraries
           'compressionstrategy': pyorc.CompressionStrategy.SPEED, # compression to be used in orc, see pyorc.CompressionStrategy (Speed = 0, COMPRESSION = 1)
           'blocksize': 65536,# block size of an ORC bloc
           'batchsize': 1024, # batch size
           'stripesize': 67108864, # stripe size
           'recordcache': 10000, # how many records should be written at once, the higher the better the compression, but the more memory is needed, potentially also bloom filter performance can be increased with higher values
           'schemastring': "struct<text:string,author:list<string>,tags:list<string>>", # Mandatory to specify schema. Please name your fields exactly like you name them in your items. See also https://pyorc.readthedocs.io/en/latest/api.html#pyorc.Struct
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'bloomfiltercolumns': None, # Define for which columns a bloom filter should be used (list). Bloom filters are very useful for performing access to columns containing few discrete values
           'bloomfilterfpp': 0.05, # False positives probability for bloom filters
           'converters': None, # Define converters, can be a dictionary, where the keys are pyorc.TypeKind and the values are subclasses of ORCConverter
           'metadata': None # metadata to be added to ORC file value is bytes (e.g. (extra="info".encode() will lead to {'extra': b'info'}))
        },
    }
}

Example S3 file, e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.orc

FEEDS = {
's3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.orc': {
        'format': 'orc',
        'encoding': 'utf8',
        'store_empty': False,
        'item_export_kwargs': {
           'compression': pyorc.CompressionKind.ZLIB, # compression to be used in orc, see pyorc.CompressionKind (None = 0, ZLIB = 1, SNAPPY = 2 (package: python-snappy), LZO = 3 (package: lzo), LZ4 = 4 (package: lz4), ZSTD = 5 (package: zstandard), note: compression may require additional libraries
           'compressionstrategy': pyorc.CompressionStrategy.SPEED, # compression to be used in orc, see pyorc.CompressionStrategy (Speed = 0, COMPRESSION = 1)
           'blocksize': 65536,# block size of an ORC bloc
           'batchsize': 1024, # batch size
           'stripesize': 67108864, # stripe size
           'recordcache': 10000, # how many records should be written at once, the higher the better the compression, but the more memory is needed, potentially also bloom filter performance can be increased with higher values
           'schemastring': "struct<text:string,author:list<string>,tags:list<string>>", # Mandatory to specify schema. Please name your fields exactly like you name them in your items. See also https://pyorc.readthedocs.io/en/latest/api.html#pyorc.Struct
           'convertallstrings': False,# convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
           'bloomfiltercolumns': None, # Define for which columns a bloom filter should be used (list). Bloom filters are very useful for performing access to columns containing few discrete values
           'bloomfilterfpp': 0.05, # False positives probability for bloom filters
           'converters': None, # Define converters, can be a dictionary, where the keys are pyorc.TypeKind and the values are subclasses of ORCConverter
           'metadata': None # metadata to be added to ORC file value is bytes (e.g. (extra="info".encode() will lead to {'extra': b'info'}))
        },
    }
}


see: https://docs.scrapy.org/en/latest/topics/exporters.html
"""

from scrapy.exporters import BaseItemExporter
from scrapy.utils.project import get_project_settings


import logging

SUPPORTED_EXPORTERS = {}
### Check which libraries are available for the exporters
try:
    from fastparquet import write as fp_write
    import pandas as pd

    SUPPORTED_EXPORTERS["parquet"] = True
    logging.getLogger().info(
        "Successfully imported fastparquet. Export to parquet supported."
    )
except ImportError:
    SUPPORTED_EXPORTERS["parquet"] = False

try:
    from fastavro import writer as fa_writer, parse_schema as fa_parse_schema

    SUPPORTED_EXPORTERS["avro"] = True
    logging.getLogger().info(
        "Successfully imported fastavro. Export to avro supported."
    )
except ImportError:
    SUPPORTED_EXPORTERS["avro"] = False

try:
    import pyorc

    SUPPORTED_EXPORTERS["orc"] = True
    logging.getLogger().info("Successfully imported pyorc. Export to orc supported.")
except ImportError:
    SUPPORTED_EXPORTERS["orc"] = False


class ParquetItemExporter(BaseItemExporter):
    """
    Parquet exporter
    """

    def __init__(self, file, dont_fail=False, **kwargs):
        """
        Initialize exporter
        """
        super().__init__(**kwargs)
        self.file = file  # file name
        self.itemcount = 0  # initial item count
        self.columns = []  # initial columns to export
        self.logger = logging.getLogger()
        self._configure(kwargs, dont_fail=dont_fail)

    def _configure(self, options, dont_fail=False):
        """Configure the exporter by poping options from the ``options`` dict.
        If dont_fail is set, it won't raise an exception on unexpected options
        (useful for using with keyword arguments in subclasses ``__init__`` methods)
        """
        self.encoding = options.pop("encoding", None)
        self.fields_to_export = options.pop("fields_to_export", None)
        self.export_empty_fields = options.pop("export_empty_fields", False)
        # Read settings
        self.pq_compression = options.pop("compression", "GZIP")
        self.pq_times = options.pop("times", "int64")
        self.pq_objectencoding = options.pop("objectencoding", "infer")
        self.pq_convertstr = options.pop("convertallstrings", False)
        self.pq_hasnulls = options.pop("hasnulls", True)
        self.pq_writeindex = options.pop("writeindex", False)
        self.pq_items_rowgroup = options.pop("items_rowgroup", 10000)
        self.pq_rowgroupoffset = options.pop("rowgroupoffset", 50000000)

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        # Initialize writer
        if len(self.columns) == 0:
            self._init_table(item)
        # Create a new row group to write
        if self.itemcount > self.pq_items_rowgroup:
            self._flush_table()
        # Add the item to data frame
        self.df = pd.concat(
            [self.df if not self.df.empty else None, self._get_df_from_item(item)]
        )
        self.itemcount += 1
        return item

    def start_exporting(self):
        """
        Triggered when Scrapy starts exporting. Useful to configure headers etc.
        """
        if not SUPPORTED_EXPORTERS["parquet"]:
            raise RuntimeError(
                "Error: Cannot export to parquet. Cannot import fastparquet. Have you installed it?"
            )
        self.firstBlock = True  # first block of parquet file

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        self._flush_table()

    def _get_columns(self, item):
        """
        Determines the columns of an item
        """
        if isinstance(item, dict):
            # for dicts try using fields of the first item
            self.columns = list(item.keys())
        else:
            # use fields declared in Item
            self.columns = list(item.fields.keys())

    def _init_table(self, item):
        """
        Initializes table for parquet file
        """
        # initialize columns
        self._get_columns(item)
        self._reset_rowgroup()

    def _get_df_from_item(self, item):
        """
        Get the dataframe from item
        """
        row = {}
        fields = dict(
            self._get_serialized_fields(item, default_value="", include_empty=True)
        )
        for column in self.columns:
            if self.pq_convertstr == True:
                row[column] = str(fields.get(column, None))
            else:
                value = fields.get(column, None)
                row[column] = value
        if self.pq_convertstr == True:
            return pd.DataFrame(row, index=[0]).astype(str)
        return pd.DataFrame.from_dict([row])

    def _reset_rowgroup(self):
        """
        Reset dataframe for writing
        """
        if self.pq_convertstr == False:  # auto determine schema
            # initialize df
            self.df = pd.DataFrame(columns=self.columns)
        else:
            # initialize df with zero strings to derive correct schema
            self.df = pd.DataFrame(columns=self.columns).astype(str)

    def _flush_table(self):
        """
        Writes the current row group to parquet file
        """
        if len(self.df.index) > 0:
            # reset written entries
            self.itemcount = 0
            # write existing dataframe as rowgroup to parquet file
            papp = True
            if self.firstBlock == True:
                self.firstBlock = False
                papp = False
            fp_write(
                self.file.name,
                self.df,
                append=papp,
                compression=self.pq_compression,
                has_nulls=self.pq_hasnulls,
                write_index=self.pq_writeindex,
                file_scheme="simple",
                object_encoding=self.pq_objectencoding,
                times=self.pq_times,
                row_group_offsets=self.pq_rowgroupoffset,
            )
            # initialize new data frame for new row group
            self._reset_rowgroup()


class AvroItemExporter(BaseItemExporter):
    """
    Avro exporter
    """

    def __init__(self, file, dont_fail=False, **kwargs):
        """
        Initialize exporter
        """
        super().__init__(**kwargs)
        self.firstBlock = True
        self.file = file  # file name
        self.itemcount = 0  # initial item count
        self.records = []  # record cache
        self.logger = logging.getLogger()
        self._configure(kwargs, dont_fail=dont_fail)

    def _configure(self, options, dont_fail=False):
        """Configure the exporter by poping options from the ``options`` dict.
        If dont_fail is set, it won't raise an exception on unexpected options
        (useful for using with keyword arguments in subclasses ``__init__`` methods)
        """
        self.encoding = options.pop("encoding", None)
        self.fields_to_export = options.pop("fields_to_export", None)
        self.export_empty_fields = options.pop("export_empty_fields", False)
        # Read settings
        self.avro_compression = options.pop("compression", "deflate")
        self.avro_compressionlevel = options.pop("compressionlevel", None)
        self.avro_convertstr = options.pop("convertallstrings", False)
        self.avro_schema = options.pop("avroschema", "")
        if self.avro_schema == "":
            raise RuntimeError("No avro schema defined")
        self.avro_parsedschema = None
        self.avro_validator = options.pop("validator", None)
        self.avro_syncinterval = options.pop("syncinterval", 16000)
        self.avro_syncmarker = options.pop("syncmarker", None)
        self.avro_recordcache = options.pop("recordcache", 10000)
        self.avro_metadata = options.pop("metadata")

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        if self.avro_parsedschema is None:
            self.avro_parsedschema = fa_parse_schema(self.avro_schema)
        # flush cache to avro file
        if self.itemcount > self.avro_recordcache:
            self._flush_table()
        record = self._get_dict_from_item(item)
        self.records.append(record)
        self.itemcount += 1
        return item

    def start_exporting(self):
        """
        Triggered when Scrapy starts exporting. Useful to configure headers etc.
        """
        if not SUPPORTED_EXPORTERS["avro"]:
            raise RuntimeError(
                "Error: Cannot export to avro. Cannot import fastavro. Have you installed it?"
            )

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        # flush last items from records cache
        self._flush_table()
        # close any open file
        self.file.close()

    def _flush_table(self):
        """
        Writes the current record cache to avro file
        """
        if len(self.records) > 0:
            if self.firstBlock == False:
                # reopen file
                self.file.close()
                self.file = open(self.file.name, "a+b")
            # write cache to avro file
            fa_writer(
                self.file,
                self.avro_parsedschema,
                self.records,
                codec=self.avro_compression,
                sync_interval=self.avro_syncinterval,
                metadata=self.avro_metadata,
                validator=self.avro_validator,
                sync_marker=self.avro_syncmarker,
                codec_compression_level=self.avro_compressionlevel,
            )
            # reset written entries
            self.itemcount = 0
            # initialize new record cache
            self.records = []
            # reinit file
            self.firstBlock = False

    def _get_dict_from_item(self, item):
        """
        Returns the columns and values from the item
        """
        fields = dict(
            self._get_serialized_fields(item, default_value="", include_empty=True)
        )
        if self.avro_convertstr:
            for column in fields:
                fields[column] = str(fields.column)
        return fields


class OrcItemExporter(BaseItemExporter):
    """
    Orc exporter
    """

    def __init__(self, file, dont_fail=False, **kwargs):
        """
        Initialize exporter
        """
        super().__init__(**kwargs)
        self.file = file  # file name
        self.itemcount = 0  # initial item count
        self.records = []  # record cache
        self.logger = logging.getLogger()
        if SUPPORTED_EXPORTERS["orc"]:
            self._configure(kwargs, dont_fail=dont_fail)

    def _configure(self, options, dont_fail=False):
        """Configure the exporter by poping options from the ``options`` dict.
        If dont_fail is set, it won't raise an exception on unexpected options
        (useful for using with keyword arguments in subclasses ``__init__`` methods)
        """
        self.encoding = options.pop("encoding", None)
        self.fields_to_export = options.pop("fields_to_export", None)
        self.export_empty_fields = options.pop("export_empty_fields", False)
        # Read settings
        self.orc_compression = options.pop("compression", pyorc.CompressionKind.ZLIB)
        self.orc_compressionstrategy = options.pop(
            "compressionstrategy", pyorc.CompressionStrategy.SPEED
        )
        self.orc_blocksize = options.pop("blocksize", 65536)
        self.orc_batchsize = options.pop("batchsize", 1024)
        self.orc_stripesize = options.pop("stripesize", 67108864)
        self.orc_recordcache = options.pop("recordcache", 10000)
        self.orc_convertstr = options.pop("convertallstrings", False)
        self.orc_schemastring = options.pop("schemastring", "")
        if self.orc_schemastring == "":
            raise RuntimeError("No orc schema defined")
        self.orc_bloomfiltercolumns = options.pop("bloomfiltercolumns", None)
        self.orc_bloomfilterfpp = options.pop("bloomfilterfpp", 0.05)
        self.orc_converters = options.pop("converters", None)
        self.orc_metadata = options.pop("metadata", None)

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        # flush cache to orc file
        if self.itemcount > self.orc_recordcache:
            self._flush_table()
        itemrecord = self._get_dict_from_item(item)
        self.records.append(itemrecord)
        self.itemcount += 1
        return item

    def start_exporting(self):
        """
        Triggered when Scrapy starts exporting. Useful to configure headers etc.
        """
        if not SUPPORTED_EXPORTERS["orc"]:
            raise RuntimeError(
                "Error: Cannot export to orc. Cannot import pyorc. Have you installed it?"
            )
        self.orcwriter = pyorc.Writer(
            self.file,
            schema=self.orc_schemastring,
            batch_size=self.orc_batchsize,
            stripe_size=self.orc_stripesize,
            compression=self.orc_compression,
            compression_strategy=self.orc_compressionstrategy,
            compression_block_size=self.orc_blocksize,
            bloom_filter_columns=self.orc_bloomfiltercolumns,
            bloom_filter_fpp=self.orc_bloomfilterfpp,
            struct_repr=pyorc.StructRepr.DICT,
            converters=self.orc_converters,
        )

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        # flush last items from records cache
        self._flush_table()
        # close any open file
        self.orcwriter.close()
        self.file.close()

    def _flush_table(self):
        """
        Writes the current record cache to avro file
        """
        if len(self.records) > 0:
            # write cache to orc file
            self.orcwriter.writerows(self.records)

            # reset written entries
            self.itemcount = 0
            # initialize new record cache
            self.records = []

    def _get_dict_from_item(self, item):
        """
        Returns the columns and values from the item
        """
        fields = dict(
            self._get_serialized_fields(item, default_value="", include_empty=True)
        )
        if self.orc_convertstr:
            for column in fields:
                fields[column] = str(fields.column)
        return fields
