# -*- coding: utf-8 -*-

from odoo.tests import common
from datetime import date


class TestOldBirthdays(common.TransactionCase):

    def test_old_birthday_events(self):
        test_cases = [
            (date(2017, 5, 16), '2017-05-05', 14, None),
            (date(2017, 2, 16), '2017-02-03', 14, None),
            (date(2017, 3, 16), '2017-03-01', 14, None)
        ]
        for i in test_cases:
            today = i[0]
            event = self.env['hr.birthday'].create({
                'birthday_date': [1],
                'birthday_employee': 'Jonas Sladkevicius',
                'active': True
                })
            old_event = event.get_old_birthdays(today, i[2])
            self.assertEqual(old_event, i[3])
