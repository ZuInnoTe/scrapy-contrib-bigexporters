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
Possible options in settings.py and their default settings
EXPORTER_PARQUET_COMPRESSION = 'GZIP' # compression to be used in Parquet, UNCOMPRESSED, GZIP, SNAPPY (package: python-snappy), LZO (package: lzo), BROTLI (package: brotli), LZ4 (package: lz4), ZSTD (package: zstandard) note: compression may require additional libraries
EXPORTER_PARQUET_TIMES = 'int64' # type for times int64 or int96, spark is int96 only
EXPORTER_PARQUET_CONVERTALLSTRINGS = True # convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
EXPORTER_PARQUET_HASNULLS = True # can contain nulls
EXPORTER_PARQUET_WRITEINDEX = False # write index as extra column
EXPORTER_PARQUET_ROWGROUPOFFSET = 50000000 # offset row groups
EXPORTER_PARQUET_ITEMS_ROWGROUP = 10000  # how many items per rowgroup, should be several thousands, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file
Custom parquet feed exporter
FEED_EXPORTERS={'parquet': 'zuinnote.scrapy.contrib.bigexporters.ParquetItemExporter'} # register additional format
Example local file:
FEEDS = {'data-%(name)s-%(time)s.parquet': {'format':'parquet','encoding':'utf8',store_empty': False}} # store as local file containing spider name and scrape datetime, e.g. data-quotes-2020-01-01T10-00-00.parquet
Example s3 file:
FEEDS = {'s3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.parquet': {'format':'parquet','encoding':'utf8',store_empty': False}} # store as s3 file containing spider name and scrape datetime, e.g. e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.parquet

see: https://docs.scrapy.org/en/latest/topics/exporters.html
"""

"""
Avro exporter
Write export as avro file (based on fastavro - you need to add the latest version as a dependency)
Possible options in settings.py and their default settings
EXPORTER_AVRO_COMPRESSION = 'deflate' # compression to be used in Avro, null, deflate, bzip2, snappy (package: python-snappy), zstandard(package: zstandard), lz4 (package: lz4) , xz (package: backports.lzma) note: compression may require additional libraries
EXPORTER_AVRO_COMPRESSIONLEVEL = None # codec specific compression level, can be an integer if supported by codec
EXPORTER_AVRO_METADATA = None # metadata (dict)
EXPORTER_AVRO_SYNCINTERVAL = 16000 # sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
EXPORTER_AVRO_RECORDCACHE = 10000 # how many records should be written at once, the higher the better the compression, but the more memory is needed
EXPORTER_AVRO_SYNCMARKER = None # bytes, if None then a random byte string is used
EXPORTER_AVRO_CONVERTALLSTRINGS = False # convert all values to string (ignored if avro schema file is specified). recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
EXPORTER_AVRO_SCHEMASTRING = None # Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also https://fastavro.readthedocs.io/en/latest/writer.html
EXPORTER_AVRO_VALIDATOR = None # use fast avro validator when writing, can be None, True (fastavro.validation.validate or a function)
Custom avro feed exporter
FEED_EXPORTERS={'avro': 'zuinnote.scrapy.contrib.bigexporters.AvroItemExporter'} # register additional format
Example local file:
FEEDS = {'data-%(name)s-%(time)s.avro': {'format':'avro','encoding':'utf8',store_empty': False}} # store as local file containing spider name and scrape datetime, e.g. data-quotes-2020-01-01T10-00-00.avro
Example s3 file:
FEEDS = {'s3://aws_key:aws_secret@mybucket/data-%(name)s-%(time)s.avro': {'format':'avro','encoding':'utf8',store_empty': False}} # store as s3 file containing spider name and scrape datetime, e.g. e.g. s3://mybucket/data-quotes-2020-01-01T10-00-00.avro

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
    SUPPORTED_EXPORTERS['parquet']=True
    logging.getLogger().info("Successfully imported fastparquet. Export to parquet supported.")
except ImportError:
    SUPPORTED_EXPORTERS['parquet']=False

try:
    from fastavro import writer as fa_writer, parse_schema as fa_parse_schema
    SUPPORTED_EXPORTERS['avro']=True
    logging.getLogger().info("Successfully imported fastavro. Export to avro supported.")
except ImportError:
    SUPPORTED_EXPORTERS['avro']=False


"""
  Parquet exporter
"""

class ParquetItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        """
            Initialize exporter
        """
        super().__init__(**kwargs)
        self.file=file # file name
        self.itemcount=0 # initial item count
        self.columns=[] # initial columns to export
        self.logger = logging.getLogger()


    def export_item(self, item):
        """
            Export a specific item to the file
        """
        # Initialize writer
        if len(self.columns)==0:
            self._init_table(item)
        # Create a new row group to write
        if self.itemcount>self.pq_items_rowgroup:
            self._flush_table()
        # Add the item to data frame
        self.df=self.df.append(self._get_df_from_item(item),ignore_index=True)
        self.itemcount+=1
        return item


    def start_exporting(self):
        """
            Triggered when Scrapy starts exporting. Useful to configure headers etc.
        """
        if not SUPPORTED_EXPORTERS['parquet']:
            raise RuntimeError("Error: Cannot export to parquet. Cannot import fastparquet. Have you installed it?")
        self.firstBlock=True # first block of parquet file
        self.settings=get_project_settings()
        self.pq_compression=self.settings.get('EXPORTER_PARQUET_COMPRESSION')
        self.pq_times=self.settings.get('EXPORTER_PARQUET_TIMES')
        if self.pq_times is None:
            self.pq_times="int64"
        self.pq_convertstr=self.settings.get('EXPORTER_PARQUET_CONVERTALLSTRINGS')
        if self.pq_convertstr is None:
            self.pq_convertstr=True
        self.pq_hasnulls=self.settings.get('EXPORTER_PARQUET_HASNULLS')
        if self.pq_hasnulls is None:
            self.pq_hasnulls=True
        self.pq_writeindex=self.settings.get('EXPORTER_PARQUET_WRITEINDEX')
        if self.pq_writeindex is None:
            self.pq_writeindex=False
        self.pq_items_rowgroup=self.settings.get('EXPORTER_PARQUET_ITEMS_ROWGROUP')
        if self.pq_items_rowgroup is None:
            self.pq_items_rowgroup=10000
        self.pq_rowgroupoffset=self.settings.get('EXPORTER_PARQUET_ROWGROUPOFFSET')
        if self.pq_rowgroupoffset is None:
            self.pq_rowgroupoffset=50000000


    def finish_exporting(self):
        """
            Triggered when Scrapy ends exporting. Useful to shutdown threads, close files etc.
        """
        self._flush_table()

    def _get_columns(self,item):
        """
         Determines the columns of an item
        """
        if isinstance(item, dict):
        # for dicts try using fields of the first item
            self.columns= list(item.keys())
        else:
            # use fields declared in Item
            self.columns = list(item.fields.keys())


    def _init_table(self,item):
        """
            Initializes table for parquet file
        """
        # initialize columns
        self._get_columns(item)
        self._reset_rowgroup()



    def _get_df_from_item(self,item):
        """
            Get the dataframe from item
        """
        row={}
        fields = dict(self._get_serialized_fields(item, default_value="",include_empty=True))
        for column in self.columns:
            if self.pq_convertstr==True:
                row[column]=str(fields.get(column,None))
            else:
                value=fields.get(column,None)
                row[column]=value
        if self.pq_convertstr==True:
          return pd.DataFrame(row,index=    [0]).astype(str)
        return row

    def _reset_rowgroup(self):
        """
            Reset dataframe for writing
        """
        if self.pq_convertstr==False: # auto determine schema
            # initialize df
            self.df= pd.DataFrame(columns=self.columns)
        else:
            # initialize df with zero strings to derive correct schema
            self.df= pd.DataFrame(columns=self.columns).astype(str)



    def _flush_table(self):
        """
            Writes the current row group to parquet file
        """
        if len(self.df.index)>0:
            # reset written entries
            self.itemcount=0
            # write existing dataframe as rowgroup to parquet file
            papp=True
            if self.firstBlock==True:
                self.firstBlock=False
                papp=False
            fp_write(self.file.name, self.df,append=papp,compression=self.pq_compression,has_nulls=self.pq_hasnulls,write_index=self.pq_writeindex,file_scheme="simple",object_encoding="infer",times=self.pq_times,row_group_offsets=self.pq_rowgroupoffset)
            # initialize new data frame for new row group
            self._reset_rowgroup()

"""
  Avro exporter
"""
class AvroItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        """
            Initialize exporter
        """
        super().__init__(**kwargs)
        self.firstBlock=True
        self.file=file # file name
        self.itemcount=0 # initial item count
        self.records=[] # record cache
        self.logger = logging.getLogger()


    def export_item(self, item):
        """
            Export a specific item to the file
        """
        if self.avro_parsedschema is None:
            self.avro_parsedschema=fa_parse_schema(self.avro_schemastring)
        # flush cache to avro file
        if self.itemcount>self.avro_recordcache:
                self._flush_table()
        record=self._get_dict_from_item(item)
        self.records.append(record)
        self.itemcount+=1
        return item


    def start_exporting(self):
        """
            Triggered when Scrapy starts exporting. Useful to configure headers etc.
        """
        if not SUPPORTED_EXPORTERS['avro']:
            raise RuntimeError("Error: Cannot export to avro. Cannot import fastavro. Have you installed it?")
        # Read settings
        self.settings=get_project_settings()
        self.avro_compression=self.settings.get('EXPORTER_AVRO_COMPRESSION')
        if self.avro_compression is None:
            self.avro_compression='deflate'
        self.avro_compressionlevel=self.settings.get('EXPORTER_AVRO_COMPRESSIONLEVEL')
        self.avro_convertstr=self.settings.get('EXPORTER_AVRO_CONVERTALLSTRINGS')
        if self.avro_convertstr is None:
            self.avro_convertstr=False
        self.avro_schemastring=self.settings.get('EXPORTER_AVRO_SCHEMASTRING')
        if self.avro_schemastring is None:
            self.avro_schemastring=''
        if self.avro_schemastring=='':
            raise RuntimeError("No avro schema defined")
        self.avro_parsedschema=None
        self.avro_validator=self.settings.get('EXPORTER_AVRO_VALIDATOR')
        self.avro_syncinterval=self.settings.get('EXPORTER_AVRO_SYNCINTERVAL')
        if self.avro_syncinterval is None:
            self.avro_syncinterval=16000
        self.avro_syncmarker=self.settings.get('EXPORTER_AVRO_SYNCMARKER')
        self.avro_recordcache=self.settings.get('EXPORTER_AVRO_RECORDCACHE')
        if self.avro_recordcache is None:
            self.avro_recordcache=10000
        self.avro_metadata=self.settings.get('EXPORTER_AVRO_METADATA')

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
            if len(self.records)>0:
                if self.firstBlock==False:
                    # reopen file
                    self.file=open(self.file.name,'a+b')
                # write cache to avro file
                fa_writer(self.file, self.avro_parsedschema,self.records,codec=self.avro_compression,sync_interval=self.avro_syncinterval,metadata=self.avro_metadata,validator=self.avro_validator,sync_marker=self.avro_syncmarker,codec_compression_level=self.avro_compressionlevel)
                # reset written entries
                self.itemcount=0
                # initialize new record cache
                self.records=[]
                # reinit file
                self.firstBlock=False


    def _infer_item_avroschema(self,item):
        """
            Infers from item the avro schema. Note: This is a heuristic and requires that always all item attributes are filled.
            We strongly recommend to not use it and specify a schema
        """
        avro_schema_dict = {}
        avro_schema_dict['namespace']=self.avro_inferschema_namespace
        avro_schema_dict['name']=self.avro_inferschema_name
        avro_schema_dict['doc']=self.avro_inferschema_doc
        avro_schema_dict['type']="record"


    def _get_dict_from_item(self,item):
        """
            Returns the columns and values from the item
        """
        fields = dict(self._get_serialized_fields(item, default_value="",include_empty=True))
        if self.avro_convertstr:
            for column in fields:
                fields[column]=str(fields.column)
        return fields
