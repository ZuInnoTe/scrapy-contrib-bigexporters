# Scrapy settings for quotes_orc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "quotes_orc"

SPIDER_MODULES = ["quotes_orc.spiders"]
NEWSPIDER_MODULE = "quotes_orc.spiders"

# import pyorc
import pyorc

# Custom orc feed exporter
FEED_EXPORTERS = {
    "orc": "zuinnote.scrapy.contrib.bigexporters.OrcItemExporter"
}  # register additional format

# Bigexporters Orc settings
FEEDS = {
    "data.orc": {
        "format": "orc",
        "encoding": "utf8",
        "store_empty": False,
        "item_export_kwargs": {
            "compression": pyorc.CompressionKind.ZLIB,  # compression to be used in orc, see pyorc.CompressionKind (None = 0, ZLIB = 1, SNAPPY = 2 (package: python-snappy), LZO = 3 (package: lzo), LZ4 = 4 (package: lz4), ZSTD = 5 (package: zstandard), note: compression may require additional libraries
            "compressionstrategy": pyorc.CompressionStrategy.SPEED,  # compression to be used in orc, see pyorc.CompressionStrategy (Speed = 0, COMPRESSION = 1)
            "blocksize": 65536,  # block size of an ORC bloc
            "batchsize": 1024,  # batch size
            "stripesize": 67108864,  # stripe size
            "recordcache": 10000,  # how many records should be written at once, the higher the better the compression, but the more memory is needed, potentially also bloom filter performance can be increased with higher values
            "schemastring": "struct<text:string,author:array<string>,tags:array<string>>",  # Mandatory to specify schema. Please name your fields exactly like you name them in your items. See also https://pyorc.readthedocs.io/en/latest/api.html#pyorc.Struct
            "convertallstrings": False,  # convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
            "bloomfiltercolumns": None,  # Define for which columns a bloom filter should be used (list). Bloom filters are very useful for performing access to columns containing few discrete values
            "bloomfilterfpp": 0.05,  # False positives probability for bloom filters
            "converters": None,  # Define converters, can be a dictionary, where the keys are pyorc.TypeKind and the values are subclasses of ORCConverter
            "metadata": None,  # metadata to be added to ORC file value is bytes (e.g. (extra="info".encode() will lead to {'extra': b'info'}))
        },
    }
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quotes_orc (+http://www.yourdomain.com)'

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
#    'quotes_orc.middlewares.QuotesOrcSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'quotes_orc.middlewares.QuotesOrcDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'quotes_orc.pipelines.QuotesOrcPipeline': 300,
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
