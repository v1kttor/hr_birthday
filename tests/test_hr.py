# -*- coding: utf-8 -*-

from datetime import date
from odoo.tests import common


class TestHrEmployee(common.TransactionCase):

    def test_upcoming_birthday(self):
        test_cases = [
            (date(2017, 2, 15), '1987-02-18', 5, date(2017, 2, 18)),
            (date(2017, 2, 15), '1987-03-18', 5, None),
            (date(1990, 2, 18), '1987-04-18', 10, None),
            (date(2017, 2, 15), None, 5, None),
            (date(2018, 3, 20), '1980-05-22', 3, None),
        ]
        for today, birthday, remind_days, expectation in test_cases:
            employee = self.env['hr.employee'].create({
                'birthday': birthday,
                'name': 'Jonas Jonaitis'})
            employee_birthday = employee.get_upcoming_birthday_date(
                remind_days, today)
            self.assertEqual(employee_birthday, expectation)
