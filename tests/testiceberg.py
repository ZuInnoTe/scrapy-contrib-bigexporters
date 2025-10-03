"""
Copyright (c) 2025 ZuInnoTe (Jörn Franke) <oss@zuinnote.eu>

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

import unittest
import tempfile
import datetime
import json
import os
import shutil

import scrapy
from pyiceberg.catalog import load_catalog
import numpy as np
from scrapy.loader import ItemLoader
from zuinnote.scrapy.contrib.bigexporters import IcebergItemExporter
from .testitem import TestItem


class TestIcebergItemExporter(unittest.TestCase):
    def setUp(self):
        # open temporary file (result)
        fd, filename = tempfile.mkstemp()
        self.filename = filename
        self.fd = fd
        self.file = open(filename, "wb")
        # open temporary directory (warehouse)
        self.tempdirectory = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.tempdirectory, "warehouse"))
        # Define catalog configuration
        self.test_catalog_configuration = {
            "default": {
                "type": "sql",
                "uri": f"sqlite:///{self.tempdirectory}/pyiceberg_catalog.db",
                "warehouse": f"file://{self.tempdirectory}/warehouse",
            }
        }
        # Define table name
        self.test_table_name = "mynamespace.scraping_data"

    def tearDown(self):
        # close file
        self.file.close()

        os.close(self.fd)
        if os.path.exists(self.filename):
            os.remove(self.filename)
        # remove temp directory directory
        shutil.rmtree(self.tempdirectory)

    def test_iceberg_export_type_schema(self):
        """
        Test if file is correctly written with native Python data types
        """
        # create exporter
        itemExporter = IcebergItemExporter(
            file=self.file,
            no_items_batch=10000,
            hasnulls=True,
            convertallstrings=False,
            iceberg_catalog=self.test_catalog_configuration,
            iceberg_namespace={
                "name": "mynamespace",
                "create_if_not_exists": True,
                "properties": {},
            },
            iceberg_table={
                "name": f"{self.test_table_name}",
                "create_if_not_exists": True,
                "properties": {},
            },
        )
        self.export_type_schema(itemExporter)

    def test_iceberg_export_string_schema(self):
        """
        Test if file is correctly written with strings
        """
        # create exporter
        itemExporter = IcebergItemExporter(
            file=self.file,
            no_items_batch=10000,
            hasnulls=True,
            convertallstrings=True,
            iceberg_catalog=self.test_catalog_configuration,
            iceberg_namespace={
                "name": "mynamespace",
                "create_if_not_exists": True,
                "properties": {},
            },
            iceberg_table={
                "name": f"{self.test_table_name}",
                "create_if_not_exists": True,
                "properties": {},
            },
        )
        self.export_string_schema(itemExporter)

    def test_iceberg_export_type_schema_recordcache(self):
        """
        Tests if all records are written even if number is larger than record cache
        """
        # create exporter
        itemExporter = IcebergItemExporter(
            file=self.file,
            no_items_batch=3,
            hasnulls=True,
            convertallstrings=False,
            iceberg_catalog=self.test_catalog_configuration,
            iceberg_namespace={
                "name": "mynamespace",
                "create_if_not_exists": True,
                "properties": {},
            },
            iceberg_table={
                "name": f"{self.test_table_name}",
                "create_if_not_exists": True,
                "properties": {},
            },
        )
        self.export_type_schema(itemExporter)

    def export_type_schema(self, itemExporter):
        itemExporter.start_exporting()
        # create and write some test data
        num_records = 10
        for i in range(num_records):
            l = ItemLoader(TestItem())
            l.add_value("ftext", "this is a test text")
            l.add_value("ftext_array", ["test1", "test2", "test3", "test4"])
            l.add_value("ffloat", float(2.5))
            l.add_value("fint", int(10))
            l.add_value("fbool", False)
            datetime_str = "2020-02-29T11:12:13"
            datetime_fmt = "%Y-%m-%dT%H:%M:%S"
            datetime_obj = datetime.datetime.strptime(datetime_str, datetime_fmt)
            l.add_value("fdatetime", datetime_obj.timestamp())
            itemExporter.export_item(l.load_item())
        itemExporter.finish_exporting()
        self.file.close()
        # reread file and compare results
        rcount = 0
        test_catalog_data = next(iter(self.test_catalog_configuration.items()))
        test_result_catalog = load_catalog(test_catalog_data[0], **test_catalog_data[1])
        test_result_table = test_result_catalog.load_table(self.test_table_name)
        df = test_result_table.scan().to_pandas()
        for indx, record in df.iterrows():
            self.assertEqual(
                "this is a test text",
                record.get("ftext", None),
                msg="String data is read correctly",
            )
            self.assertIsNone(
                np.testing.assert_array_equal(
                    ["test1", "test2", "test3", "test4"],
                    record.get("ftext_array", None),
                ),
                msg="String array data is read correctly",
            )
            self.assertEqual(
                float(2.5),
                record.get("ffloat", None),
                msg="Float data is read correctly",
            )
            self.assertEqual(
                int(10), record.get("fint", None), msg="Int data is read correctly"
            )
            self.assertFalse(
                record.get("fbool", None), msg="Bool data is read correctly"
            )
            self.assertEqual(
                datetime_str,
                datetime.datetime.fromtimestamp(record.get("fdatetime", None)).strftime(
                    datetime_fmt
                ),
                msg="DateTime data is read correctly",
            )
            rcount += 1
        self.assertEqual(
            rcount,
            10,
            msg="Number of records read corresponds to number of records written",
        )
        # check if result summary is correctly written
        with open(self.filename, "rb") as f:
            d = json.load(f)
            self.assertEqual(
                d["noitems"],
                10,
                msg="Number of records read corresponds to number of records written",
            )

    def export_string_schema(self, itemExporter):
        itemExporter.start_exporting()
        # create and write some test data
        num_records = 10
        for i in range(num_records):
            l = ItemLoader(TestItem())
            l.add_value("ftext", "this is a test text")
            l.add_value("ftext_array", ["test1", "test2", "test3", "test4"])
            l.add_value("ffloat", float(2.5))
            l.add_value("fint", int(10))
            l.add_value("fbool", False)
            datetime_str = "2020-02-29T11:12:13"
            datetime_fmt = "%Y-%m-%dT%H:%M:%S"
            datetime_obj = datetime.datetime.strptime(datetime_str, datetime_fmt)
            l.add_value(
                "fdatetime",
                datetime_obj.replace(tzinfo=datetime.timezone.utc).timestamp(),
            )
            itemExporter.export_item(l.load_item())
        itemExporter.finish_exporting()
        self.file.close()
        # reread file and compare results
        rcount = 0
        test_catalog_data = next(iter(self.test_catalog_configuration.items()))
        test_result_catalog = load_catalog(test_catalog_data[0], **test_catalog_data[1])
        test_result_table = test_result_catalog.load_table(self.test_table_name)
        df = test_result_table.scan().to_pandas()
        for indx, record in df.iterrows():
            self.assertEqual(
                "this is a test text",
                record.get("ftext", None),
                msg="String data is read correctly",
            )
            self.assertEqual(
                "['test1', 'test2', 'test3', 'test4']",
                record.get("ftext_array", None),
                msg="String array data is read correctly",
            )
            self.assertEqual(
                "2.5", record.get("ffloat", None), msg="Float data is read correctly"
            )
            self.assertEqual(
                "10", record.get("fint", None), msg="Int data is read correctly"
            )
            self.assertEqual(
                "False", record.get("fbool", None), msg="Bool data is read correctly"
            )
            self.assertEqual(
                "1582974733.0",
                record.get("fdatetime", None),
                msg="DateTime data is read correctly",
            )
            rcount += 1
        self.assertEqual(
            rcount,
            10,
            msg="Number of records read corresponds to number of records written",
        )
        # check if result summary is correctly written
        with open(self.filename, "rb") as f:
            d = json.load(f)
            self.assertEqual(
                d["noitems"],
                10,
                msg="Number of records read corresponds to number of records written",
            )


if __name__ == "__main__":
    unittest.main()
