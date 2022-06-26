# Scrapy settings for quotes_avro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "quotes_avro"

SPIDER_MODULES = ["quotes_avro.spiders"]
NEWSPIDER_MODULE = "quotes_avro.spiders"

# Custom avro feed exporter
FEED_EXPORTERS = {
    "avro": "zuinnote.scrapy.contrib.bigexporters.AvroItemExporter"
}  # register additional format

# Bigexporters Avro settings
FEEDS = {
    "data.avro": {
        "format": "avro",
        "encoding": "utf8",
        "store_empty": False,
        "item_export_kwargs": {
            "compression": "deflate",  # compression to be used in Avro, null, deflate, bzip2, snappy (package: python-snappy), zstandard(package: zstandard), lz4 (package: lz4) , xz (packahe: backports.lzma) note: compression may require additional libraries
            "compressionlevel": None,  # codec specific compression level, can be an integer if supported by codec
            "metadata": None,  # metadata (dict)
            "syncinterval": 16000,  # sync interval, how many bytes written per block, should be several thousands, the higher the better is the compression, but seek time may increase
            "recordcache": 10000,  # how many records should be written at once, the higher the better the compression, but the more memory is needed
            "syncmarker": None,  # bytes, if None then a random byte string is used
            "convertallstrings": False,  # convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
            "validator": None,  # use fast avro validator when writing, can be None, True (fastavro.validation.validate or a function)
            "avroschema": {
                "doc": "Some quotes",
                "name": "quotes",
                "type": "record",
                "fields": [
                    {"name": "text", "type": "string"},
                    {
                        "name": "author",
                        "type": {"type": "array", "items": "string", "default": []},
                    },
                    {
                        "name": "tags",
                        "type": {"type": "array", "items": "string", "default": []},
                    },
                ],
            },  # Mandatory to specify schema. Please name your fields exactly like you name them in your items. Please make sure that the item has always values filled, otherwise you may see errors during scraping. See also https://fastavro.readthedocs.io/en/latest/writer.html
        },
    }
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quotes_avro (+http://www.yourdomain.com)'

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
#    'quotes_avro.middlewares.QuotesAvroSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'quotes_avro.middlewares.QuotesAvroDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'quotes_avro.pipelines.QuotesAvroPipeline': 300,
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
