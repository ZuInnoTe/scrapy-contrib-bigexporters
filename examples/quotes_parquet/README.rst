==============
quotes-parquet
==============

Install dependencies
====================

Use the following to install dependencies::

    pip install -r requirements.txt


Run Scrapy
==========

Use the following command to run the crawler in Parquet format ::

    scrapy crawl quotes_parquet -o data.parquet -t parquet
