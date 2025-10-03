==============
quotes-iceberg
==============

Install dependencies
====================

Use the following to install dependencies::

    pip install -r requirements.txt


We use here pyiceberg with the dependency for a sql-lite backed catalog. 

Run Scrapy
==========

Use the following command to run the crawler in iceberg format ::

    scrapy crawl quotes

You will get as output a table in iceberg format in a catalog in the local filesystem in the folder ./warehouse 

This table contains all the scraped items.

The file result.json simply contains the number of scraped items.
