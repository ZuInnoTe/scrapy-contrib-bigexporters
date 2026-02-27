"""
Copyright (c) 2020 ZuInnoTe (Jörn Franke) <oss@zuinnote.eu>

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
see: https://docs.scrapy.org/en/latest/topics/exporters.html
"""

from scrapy.exporters import BaseItemExporter
from scrapy.utils.project import get_project_settings

import json
import logging

import pandas as pd

SUPPORTED_EXPORTERS = {}
### Check which libraries are available for the exporters
# Parquet
try:
    import pyarrow
    import pyarrow.parquet as pq

    SUPPORTED_EXPORTERS["parquet"] = True
    logging.getLogger().info(
        "Successfully imported pyarrow.parquet. Export to parquet supported."
    )
except ImportError:
    SUPPORTED_EXPORTERS["parquet"] = False
# Orc
try:
    import pyarrow
    import pyarrow.orc

    SUPPORTED_EXPORTERS["orc"] = True
    logging.getLogger().info("Successfully imported pyarrow. Export to orc supported.")
except ImportError:
    SUPPORTED_EXPORTERS["orc"] = False

# Avro
try:
    from fastavro import writer as fa_writer, parse_schema as fa_parse_schema

    SUPPORTED_EXPORTERS["avro"] = True
    logging.getLogger().info(
        "Successfully imported fastavro. Export to avro supported."
    )
except ImportError:
    SUPPORTED_EXPORTERS["avro"] = False

# Iceberg
try:
    import pyarrow
    import pyiceberg
    from pyiceberg.catalog import load_catalog

    SUPPORTED_EXPORTERS["iceberg"] = True
    logging.getLogger().info(
        "Successfully imported pyiceberg. Export to iceberg supported."
    )
except ImportError:
    SUPPORTED_EXPORTERS["iceberg"] = False


"""
Parquet exporter
Write export as parquet file
"""


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
        ## exporter
        self.pq_convertstr = options.pop("convertallstrings", False)
        self.pq_no_items_batch = options.pop("no_items_batch", 10000)
        ## parquet
        self.pq_pyarrow_safe_schema = options.pop("pyarrow_safe_schema", True)
        self.pq_schema = options.pop("schema", None)
        self.pq_row_group_size = options.pop("row_group_size", None)
        self.pq_version = options.pop("version", "2.6")
        self.pq_use_dictionary = options.pop("use_dictionary", True)
        self.pq_compression = options.pop("compression", "zstd")
        self.pq_write_statistics = options.pop("write_statistics", True)
        self.pq_use_deprecated_int96_timestamps = options.pop(
            "use_deprecated_int96_timestamps", None
        )
        self.pq_coerce_timestamps = options.pop("coerce_timestamps", None)
        self.pq_allow_truncated_timestamps = options.pop(
            "allow_truncated_timestamps", False
        )
        self.pq_data_page_size = options.pop("data_page_size", None)
        self.pq_flavor = options.pop("flavor", None)
        self.pq_filesystem = options.pop("filesystem", None)
        self.pq_compression_level = options.pop("compression_level", None)
        self.pq_use_byte_stream_split = options.pop("use_byte_stream_split", False)
        self.pq_column_encoding = options.pop("column_encoding", None)
        self.pq_data_page_version = options.pop("data_page_version", "1.0")
        self.pq_use_compliant_nested_type = options.pop(
            "use_compliant_nested_type", True
        )
        self.pq_encryption_properties = options.pop("encryption_properties", None)
        self.pq_write_batch_size = options.pop("write_batch_size", None)
        self.pq_dictionary_pagesize_limit = options.pop(
            "dictionary_pagesize_limit", None
        )
        self.pq_store_schema = options.pop("store_schema", True)
        self.pq_write_page_index = options.pop("write_page_index", False)
        self.pq_write_page_checksum = options.pop("write_page_checksum", False)
        self.pq_sorting_columns = options.pop("sorting_columns", None)
        self.pq_store_decimal_as_integer = options.pop(
            "store_decimal_as_integer", False
        )
        self.pq_use_content_defined_chunking = options.pop(
            "use_content_defined_chunking", False
        )
        # Init writer
        self.writer = None

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        # Initialize writer
        if len(self.columns) == 0:
            self._init_table(item)
        # Create a new row group to write
        if self.itemcount > self.pq_no_items_batch:
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
                "Error: Cannot export to parquet. Cannot import pyarrow.parquet. Have you installed it?"
            )

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        self._flush_table()
        if self.writer is not None:
            self.writer.close()

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
        self._reset_dataframe()

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

    def _reset_dataframe(self):
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
            # write existing dataframe to parquet file
            if self.pq_schema is not None:
               table = pyarrow.Table.from_pandas(self.df, schema=self.pq_schema, safe=pq_pyarrow_safe_schema)
            else:
               table = pyarrow.Table.from_pandas(self.df)
            if self.writer is None:
                if self.pq_schema is None:
                    schema = table.schema
                else:
                    schema = self.pq_schema
                self.writer = pq.ParquetWriter(
                    self.file.name,
                    schema=schema,
                    version=self.pq_version,
                    use_dictionary=self.pq_use_dictionary,
                    compression=self.pq_compression,
                    write_statistics=self.pq_write_statistics,
                    use_deprecated_int96_timestamps=self.pq_use_deprecated_int96_timestamps,
                    coerce_timestamps=self.pq_coerce_timestamps,
                    allow_truncated_timestamps=self.pq_allow_truncated_timestamps,
                    data_page_size=self.pq_data_page_size,
                    flavor=self.pq_flavor,
                    filesystem=self.pq_filesystem,
                    compression_level=self.pq_compression_level,
                    use_byte_stream_split=self.pq_use_byte_stream_split,
                    column_encoding=self.pq_column_encoding,
                    data_page_version=self.pq_data_page_version,
                    use_compliant_nested_type=self.pq_use_compliant_nested_type,
                    encryption_properties=self.pq_encryption_properties,
                    write_batch_size=self.pq_write_batch_size,
                    dictionary_pagesize_limit=self.pq_dictionary_pagesize_limit,
                    store_schema=self.pq_store_schema,
                    write_page_index=self.pq_write_page_index,
                    write_page_checksum=self.pq_write_page_checksum,
                    sorting_columns=self.pq_sorting_columns,
                    store_decimal_as_integer=self.pq_store_decimal_as_integer,
                    use_content_defined_chunking=self.pq_use_content_defined_chunking,
                )
            self.writer.write_table(table, self.pq_row_group_size)
            # initialize new data frame for new row group
            self._reset_dataframe()


"""
Avro exporter
Write export as avro file
"""


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


"""
Orc exporter
Write export as orc file
"""


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
        self.columns = []  # columns to export
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
        self.orc_pyarrow_safe_schema = options.pop("pyarrow_safe_schema", True)
        self.orc_schema = options.pop("schema", None)
        ## exporter
        self.orc_convertstr = options.pop("convertallstrings", False)
        self.orc_no_items_batch = options.pop("no_items_batch", 10000)
        ## orc
        self.orc_file_version = options.pop("file_version", "0.12")
        self.orc_batch_size = options.pop("batch_size", 1024)
        self.orc_stripe_size = options.pop("stripe_size", 64 * 1024 * 1024)
        self.orc_compression = options.pop("compression", "zstd")
        self.orc_compression_block_size = options.pop(
            "compression_block_size", 64 * 1024
        )
        self.orc_compression_strategy = options.pop("compression_strategy", "speed")
        self.orc_row_index_stride = options.pop("row_index_stride", 10000)
        self.orc_padding_tolerance = options.pop("padding_tolerance", 0.0)
        self.orc_dictionary_key_size_threshold = options.pop(
            "dictionary_key_size_threshold", 0.0
        )
        self.orc_bloom_filter_columns = options.pop("bloom_filter_columns", None)
        self.orc_bloom_filter_fpp = options.pop("bloom_filter_fpp", 0.05)
        # Init writer
        self.orc_writer = None

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        # Initialize writer
        if len(self.columns) == 0:
            self._init_table(item)
        # Create a new row group to write
        if self.itemcount > self.orc_no_items_batch:
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
        if not SUPPORTED_EXPORTERS["orc"]:
            raise RuntimeError(
                "Error: Cannot export to orc. Cannot import pyarrow. Have you installed it?"
            )

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        # flush last items from records cache
        self._flush_table()
        # close any open file
        if self.orc_writer is not None:
            self.orc_writer.close()
        self.file.close()

    def _flush_table(self):
        """
        Writes the current record cache to avro file
        """
        if len(self.df.index) > 0:
            # reset written entries
            self.itemcount = 0
            # write existing dataframe as orc file
            if self.orc_schema is not None:
               table = pyarrow.Table.from_pandas(self.df, schema=self.orc_schema, safe=orc_pyarrow_safe_schema)
            else:
               table = pyarrow.Table.from_pandas(self.df)
            table = pyarrow.Table.from_pandas(self.df)
            if self.orc_writer is None:
                self.orc_writer = pyarrow.orc.ORCWriter(
                    self.file.name,
                    file_version=self.orc_file_version,
                    batch_size=self.orc_batch_size,
                    stripe_size=self.orc_stripe_size,
                    compression=self.orc_compression,
                    compression_block_size=self.orc_compression_block_size,
                    compression_strategy=self.orc_compression_strategy,
                    row_index_stride=self.orc_row_index_stride,
                    padding_tolerance=self.orc_padding_tolerance,
                    dictionary_key_size_threshold=self.orc_dictionary_key_size_threshold,
                    bloom_filter_columns=self.orc_bloom_filter_columns,
                    bloom_filter_fpp=self.orc_bloom_filter_fpp,
                )
            # write cache to orc file
            self.orc_writer.write(table)
            # initialize new data frame
            self._reset_dataframe()

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
        self._reset_dataframe()

    def _get_df_from_item(self, item):
        """
        Get the dataframe from item
        """
        row = {}
        fields = dict(
            self._get_serialized_fields(item, default_value="", include_empty=True)
        )
        for column in self.columns:
            if self.orc_convertstr == True:
                row[column] = str(fields.get(column, None))
            else:
                value = fields.get(column, None)
                row[column] = value
        if self.orc_convertstr == True:
            return pd.DataFrame(row, index=[0]).astype(str)
        return pd.DataFrame.from_dict([row])

    def _reset_dataframe(self):
        """
        Reset dataframe for writing
        """
        if self.orc_convertstr == False:  # auto determine schema
            # initialize df
            self.df = pd.DataFrame(columns=self.columns)
        else:
            # initialize df with zero strings to derive correct schema
            self.df = pd.DataFrame(columns=self.columns).astype(str)


"""
Iceberg exporter
Write export as open table format Iceberg
"""


class IcebergItemExporter(BaseItemExporter):
    """
    Iceberg exporter
    """

    def __init__(self, file, dont_fail=False, **kwargs):
        """
        Initialize exporter
        """
        super().__init__(**kwargs)
        self.file = file  # file name
        self.itemcount = 0  # initial item count
        self.totalitemcount = 0  # total item count
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
        self.pyarrow_safe_schema = options.pop("pyarrow_safe_schema", True)
        self.schema = options.pop("schema", None)
        # Read settings
        self.convertstr = options.pop("convertallstrings", False)
        self.no_items_batch = options.pop("no_items_batch", 10000)
        self.iceberg_catalog = options.pop("iceberg_catalog", {})
        self.iceberg_namespace = options.pop("iceberg_namespace", {})
        self.iceberg_table = options.pop("iceberg_table", {})
        # Validate settings
        if self.no_items_batch < 1:
            raise RuntimeError(
                "Iceberg: Number of items in batch processing cannot be smaller than 1"
            )
        # An iceberg configuration is complex and is not processed as this time. Thus, we do only a simple validation.
        if len(self.iceberg_catalog) == 0:
            logging.getLogger().warn(
                "Empty Iceberg catalog specified. Assuming that it is specified outside (e.g. using environment variables)"
            )
            self.iceberg_catalog_configuration = None
        else:
            # Read only the first item of the dict. We support only to write to one catalog at a time.
            self.iceberg_catalog_configuration = next(
                iter(self.iceberg_catalog.items())
            )
        # Iceberg namespace configuration
        if len(self.iceberg_namespace) == 0:
            raise RuntimeError(
                'Iceberg: No namespace configuration "iceberg_namespace" specified'
            )
        if self.iceberg_namespace.get("name", "") == "":
            raise RuntimeError(
                'Iceberg: No namespace name configuration "iceberg_namespace" specified'
            )
        else:
            self.iceberg_namespace_name = self.iceberg_namespace.get("name")
        self.iceberg_namespace_create_if_not_exists = self.iceberg_namespace.get(
            "create_if_not_exists", False
        )
        self.iceberg_namespace_properties = self.iceberg_namespace.get("properties", {})
        # Iceberg table configuration
        if len(self.iceberg_table) == 0:
            raise RuntimeError(
                'Iceberg: No table configuration "iceberg_table" specified'
            )
        if self.iceberg_table.get("name", "") == "":
            raise RuntimeError(
                'Iceberg: No table name configuration "iceberg_table" specified'
            )
        else:
            self.iceberg_table_name = self.iceberg_table.get("name")
        self.iceberg_table_create_if_not_exists = self.iceberg_table.get(
            "create_if_not_exists", False
        )
        self.iceberg_table_location = self.iceberg_table.get("location", None)
        self.iceberg_table_properties = self.iceberg_table.get("properties", {})

    def export_item(self, item):
        """
        Export a specific item to the file
        """
        # Initialize writer
        if len(self.columns) == 0:
            self._init_table(item)
        # Create a new row group to write
        if self.itemcount > self.no_items_batch:
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
        if not SUPPORTED_EXPORTERS["iceberg"]:
            raise RuntimeError(
                "Error: Cannot export to iceberg. Cannot import pyiceberg. Have you installed it?"
            )
        # Initialize catalog
        if self.iceberg_catalog_configuration == None:
            self.pyiceberg_catalog = load_catalog()
        else:
            self.pyiceberg_catalog = load_catalog(
                self.iceberg_catalog_configuration[0],
                **self.iceberg_catalog_configuration[1],
            )
        # Initialize namespace
        if self.iceberg_namespace_create_if_not_exists:
            self.pyiceberg_catalog.create_namespace_if_not_exists(
                self.iceberg_namespace_name, self.iceberg_namespace_properties
            )
        # Initialize table
        self.pyiceberg_table = None

    def finish_exporting(self):
        """
        Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        # write possible remaining data
        self._flush_table()
        # write json with number of items scraped
        self.file.write(
            bytearray(json.dumps({"noitems": self.totalitemcount}), "utf-8")
        )
        # close any open file
        self.file.close()

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
        Initializes table
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
            if self.convertstr == True:
                row[column] = str(fields.get(column, None))
            else:
                value = fields.get(column, None)
                row[column] = value
        if self.convertstr == True:
            return pd.DataFrame(row, index=[0]).astype(str)
        return pd.DataFrame.from_dict([row])

    def _reset_rowgroup(self):
        """
        Reset dataframe for writing
        """
        if self.convertstr == False:  # auto determine schema
            # initialize df
            self.df = pd.DataFrame(columns=self.columns)
        else:
            # initialize df with zero strings to derive correct schema
            self.df = pd.DataFrame(columns=self.columns).astype(str)

    def _flush_table(self):
        """
        Append current batch to Iceberg table
        """
        if len(self.df.index) > 0:
            # reset written entries
            self.totalitemcount += self.itemcount
            self.itemcount = 0
            # Convert to arrow
            if self.schema is not None:
               table = pyarrow.Table.from_pandas(self.df, schema=self.schema, safe=pyarrow_safe_schema)
            else:
               table = pyarrow.Table.from_pandas(self.df)
            arrow_table = pyarrow.Table.from_pandas(self.df)
            # check if table is loaded
            if self.pyiceberg_table is None:
                if self.iceberg_table_create_if_not_exists:
                    self.pyiceberg_table = (
                        self.pyiceberg_catalog.create_table_if_not_exists(
                            self.iceberg_table_name,
                            schema=arrow_table.schema,
                            location=self.iceberg_table_location,
                            properties=self.iceberg_table_properties,
                        )
                    )
                else:
                    self.iceberg_table_properties = self.pyiceberg_catalog.load_table(
                        self.iceberg_table_name
                    )
            # append data
            self.pyiceberg_table.append(arrow_table)
            # initialize new data frame for new row group
            self._reset_rowgroup()
