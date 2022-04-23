#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import individual
import unittest
from pathlib import Path
import tempfile
import shutil


class IndTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path_dir = Path(self.tmp.name)
        shutil.copyfile(individual.pathh(), self.path_dir / 'test.db')
        self.fullpath = self.path_dir / 'test.db'
        self.conn = sqlite3.connect(self.fullpath)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
                        """
                        SELECT student_name.name, students.groupt, students.grade
                        FROM students
                        INNER JOIN student_name ON student_name.student_id = students.student_id
                        WHERE student_name.student_id == 1
                        """
        )
        rows = self.cursor.fetchall()
        self.result = [
            {
                "name": row[0],
                "groupt": row[1],
                "grade": row[2],
            }
            for row in rows
        ]

    def test_create_db(self):
        self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'students' OR name = 'student_name'
            """
        )
        table = self.cursor.fetchall()
        self.assertEqual(table, [('student_name',), ('students',)])

    def test_add_student(self):
        individual.add_student(self.fullpath, 'text', 3, 'text')
        self.cursor.execute(
                        """
                        SELECT student_name.name, students.groupt, students.grade
                        FROM students
                        INNER JOIN student_name ON student_name.student_id = students.student_id
                        WHERE students.student_id = (SELECT MAX(student_id)  FROM students)
                        """
        )
        rows = self.cursor.fetchall()
        self.last = [
            {
                "name": row[0],
                "groupt": row[1],
                "grade": row[2],
            }
            for row in rows
        ]
        self.assertEqual(self.last, [{'name': 'text', 'groupt': 3, 'grade': 'text'}])

    def test1_select_student_1(self):
        self.assertListEqual(self.result, [{'name': 'Bobrov N.V', 'groupt': 1, 'grade': '5 5 5 5 5'}])

    def test1_select_student_2(self):
        self.assertNotEqual(self.result, [{'name': 'Ivanov I.I', 'groupt': 2, 'grade': '4 4 4 4 4'}])

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
