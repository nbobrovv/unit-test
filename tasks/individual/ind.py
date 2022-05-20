#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List
import sqlite3


# Класс пользовательского исключения в случае, если введенная
# команда является недопустимой.

class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Student:
    name: str
    groupt: str
    grade: str


@dataclass
class Staff:
    students: List[Student] = field(default_factory=lambda: [])

    db = sqlite3.connect('students.db')
    cur = db.cursor()
    db.commit()

    def add(self, name: str, groupt: str, grade: str) -> None:
        self.students.append(
            Student(
                name=name,
                groupt=groupt,
                grade=grade,
            )
        )
        self.students.sort(key=lambda student: student.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, student in enumerate(self.students, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.name,
                    student.groupt,
                    student.grade
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self):
        count = 0
        result = []
        # Проверить сведения студентов из списка.
        for student in self.students:
            grade = list(map(int, student.grade.split()))
            if sum(grade) / max(len(grade), 1) >= 4.0:
                count += 1
                result.append(student)
        return result

    def load(self) -> None:
        self.students = []
        data = self.cur.execute("SELECT * FROM students")
        for i in data:
            name = i[1]
            groupt= i[2]
            grade = i[3]
            self.students.append(
                Student(
                    name=name,
                    groupt=groupt,
                    grade=grade
                )
            )

    def save(self) -> None:
        self.cur.execute('''DELETE FROM students''')
        for student in self.students:
            name = student.name
            groupt = student.groupt
            grade = student.grade

            self.cur.execute('''INSERT INTO students (
                        name, groupt, grade) VALUES (?, ?, ?)
                        ''', (name, groupt, grade))
            self.db.commit()

    def kill(self) -> None:
        self.cur.execute('''DROP TABLE students''')
        self.db.commit()
