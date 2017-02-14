# -*- coding: utf-8 -*-

from odoo.tests import common
from datetime import date


class TestHrEmployee(common.TransactionCase):

    def test_upcoming_birthday(self):
        test_cases = [
            (date(2017, 2, 15), '1987-02-18', 5, date(2017, 2, 18)),
            (date(2017, 2, 15), '1987-03-18', 5, None),
            (date(1990, 2, 18), '1987-04-18', 10, None),
            (date(2017, 2, 15), None, 5, None),
            (date(2018, 3, 20), '1980-05-22', 3, None),

        ]
        for i in test_cases:
            today = i[0]
            employee = self.env['hr.employee'].create({
                'birthday': i[1],
                'name': 'Jonas Sladkevičius'})
            employee_birthday = employee.get_upcoming_birthday_date(
                i[2], today)
            self.assertEqual(employee_birthday, i[3])
