#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sqlite3
import ind

db = sqlite3.connect('ind_utest.sqlite')
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS students (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            groupt TEXT,
            grade TEXT
        )''')

cur.execute('''INSERT INTO students (
                name, groupt, grade) VALUES (?, ?, ?)
                ''', ('Nikolay', '1', '5 5 5 5 5'))
db.commit()


class StudentTest(unittest.TestCase):
    """People tests"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("")

    def test_select(self):
        """Select operation test"""
        print("id: " + self.id())
        student = ind.Staff()
        student.load()
        sel_test_v = student.select()
        res = ''
        if sel_test_v:
            for student in sel_test_v:
                res = student.name
        self.assertEqual(res, 'students')


if __name__ == '__main__':
    unittest.main()
