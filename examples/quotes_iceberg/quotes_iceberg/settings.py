# Scrapy settings for quotes_iceberg project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "quotes_iceberg"

SPIDER_MODULES = ["quotes_iceberg.spiders"]
NEWSPIDER_MODULE = "quotes_iceberg.spiders"

# Custom iceberg feed exporter
FEED_EXPORTERS = {
    "iceberg": "zuinnote.scrapy.contrib.bigexporters.IcebergItemExporter"
}  # register additional format


# Bigexporters Iceberg settings
FEEDS = {
    "result.json": {
        "format": "iceberg",
        "encoding": "utf8",
        "store_empty": False,
        "item_export_kwargs": {
            "hasnulls": True,  # can contain nulls
            "convertallstrings": False,  # convert all values to string. recommended for compatibility reasons, conversion to native types is suggested as part of the ingestion in the processing platform
            "iceberg_catalog": {
                "default": {
                    "type": "sql",
                    "uri": "sqlite:///./warehouse/pyiceberg_catalog.db",
                    "warehouse": "file://./warehouse/data",
                }
            },
            "iceberg_namespace": {
                "name": "mynamespace",
                "create_if_not_exists": True,
                "properties": {},
            },
            "iceberg_table": {
                "name": "mynamespace.scraping_data",
                "create_if_not_exists": True,
                "properties": {
                    "write.parquet.compression-codec": "zstd",
                    "write.parquet.compression-level": 3,
                },
            },
        },
    }
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quotes_iceberg (+http://www.yourdomain.com)'

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
#    'quotes_iceberg.middlewares.QuotesIcebergSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'quotes_iceberg.middlewares.QuotesIcebergDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'quotes_iceberg.pipelines.QuotesIcebergPipeline': 300,
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
