# Scrapy settings for quotes_parquet project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "quotes_parquet"

SPIDER_MODULES = ["quotes_parquet.spiders"]
NEWSPIDER_MODULE = "quotes_parquet.spiders"

# Custom parquet feed exporter
FEED_EXPORTERS = {
    "parquet": "zuinnote.scrapy.contrib.bigexporters.ParquetItemExporter"
}  # register additional format


# Bigexporters Parquet settings
FEEDS = {
    "data.parquet": {
        "format": "parquet",
        "encoding": "utf8",
        "store_empty": False,
        "item_export_kwargs": {
            "convertallstrings": False,  # convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
            "no_items_batch": 10000,  # how many items to append at once, should be several thousands, e.g. between 5,000 and 30,000. The more rows the higher the memory consumption and the better the compression on the final parquet file
            "schema": None,  # None = autodetect. Otherwise pyarrow.Schema (https://arrow.apache.org/docs/python/generated/pyarrow.Schema.html#pyarrow.Schema)
            "row_group_size": None,  # Maximum number of rows in each written row group. If None, the row group size will be the minimum of the Table size (in rows) and 1024 * 1024.
            # See following options: https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetWriter.html
            "version": "2.6",
            "use_dictionary": True,
            "compression": "zstd",
            "write_statistics": True,
            "use_deprecated_int96_timestamps": None,
            "coerce_timestamps": None,
            "allow_truncated_timestamps": False,
            "data_page_size": None,
            "flavor": None,
            "filesystem": None,
            "compression_level": 3,
            "use_byte_stream_split": False,
            "column_encoding": None,
            "data_page_version": "1.0",
            "use_compliant_nested_type": True,
            "encryption_properties": None,
            "write_batch_size": None,
            "dictionary_pagesize_limit": None,
            "store_schema": True,
            "write_page_index": False,
            "write_page_checksum": False,
            "sorting_columns": None,
            "store_decimal_as_integer": False,
            "use_content_defined_chunking": False,
        },
    }
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quotes_parquet (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'quotes_parquet.middlewares.QuotesParquetSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'quotes_parquet.middlewares.QuotesParquetDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'quotes_parquet.pipelines.QuotesParquetPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
