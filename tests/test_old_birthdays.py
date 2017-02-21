# -*- coding: utf-8 -*-

from datetime import date

from odoo.tests import common


class TestOldBirthdays(common.TransactionCase):

    def test_old_birthday_events(self):
        test_cases = [
            (date(2017, 5, 16), date(2017, 5, 1), 14),
            (date(2017, 2, 16), date(2017, 2, 1), 14),
            (date(2017, 3, 16), date(2017, 3, 1), 14)
        ]
        employee = self.env['hr.employee'].create({
            'birthday': '2017-02-17',
            'name': 'Jonas Jonaitis'})
        for today, birthday_date, days_to_false in test_cases:
            event = self.env['hr.birthday'].create({
                'birthday_date': birthday_date,
                'birthday_employee': employee.id})
            old_events = event.find_old_birthdays(today, days_to_false)
            self.assertIn(
                event, old_events, msg="Failed {0!s}".format(today))
