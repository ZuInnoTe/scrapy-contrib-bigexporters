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

import unittest
import tempfile
import datetime
import os

import scrapy
from fastparquet import ParquetFile
from scrapy.loader import ItemLoader
from zuinnote.scrapy.contrib.bigexporters import ParquetItemExporter
from .testitem import TestItem


class TestParquetItemExporter(unittest.TestCase):
    def setUp(self):
        # open file
        fd, filename = tempfile.mkstemp()
        self.filename = filename
        self.fd = fd
        self.file = open(filename, "wb")

    def tearDown(self):
        # close file
        self.file.close()

        os.close(self.fd)
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_parquet_export_type_schema(self):
        """
        Test if file is correctly written with native Python data types
        """
        # create exporter
        itemExporter = ParquetItemExporter(
            file=self.file,
            compression="GZIP",
            times="int64",
            hasnulls=True,
            convertallstrings=False,
            writeindex=False,
            objectencoding="infer",
            rowgroupoffset=50000000,
            items_rowgroup=10000,
        )
        self.export_type_schema(itemExporter)

    def test_parquet_export_string_schema(self):
        """
        Test if file is correctly written with strings
        """
        # create exporter
        itemExporter = ParquetItemExporter(
            file=self.file,
            compression="GZIP",
            times="int64",
            hasnulls=True,
            convertallstrings=True,
            writeindex=False,
            objectencoding="infer",
            rowgroupoffset=50000000,
            items_rowgroup=10000,
        )
        self.export_string_schema(itemExporter)

    def test_parquet_export_type_schema_recordcache(self):
        """
        Tests if all records are written even if number is larger than record cache
        """
        # create exporter
        itemExporter = ParquetItemExporter(
            file=self.file,
            compression="GZIP",
            times="int64",
            hasnulls=True,
            convertallstrings=False,
            writeindex=False,
            objectencoding="infer",
            rowgroupoffset=50000000,
            items_rowgroup=3,
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
        pf = ParquetFile(self.filename)
        df = pf.to_pandas()
        for indx, record in df.iterrows():
            self.assertEqual(
                "this is a test text",
                record.get("ftext", None),
                msg="String data is read correctly",
            )
            self.assertEqual(
                ["test1", "test2", "test3", "test4"],
                record.get("ftext_array", None),
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
        pf = ParquetFile(self.filename)
        df = pf.to_pandas()

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


if __name__ == "__main__":
    unittest.main()
