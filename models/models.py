# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class hrbirthday(models.Model):
    _name = 'hr_birthday.hrbirthday'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100


class Birthday(models,Model):
    _name = 'hrbirthday.birthday'

    birthday_employee = fields.Many2one('hr.employee')
    birthday_date = fields.Date()
    department_id = fields.Many2one('hr.department')
    celebration_date = fields.Datetime()
    active = fields.Boolean(default=True)

class Department(models,Model):
    _name = 'hrbirthday.department'

    check_birthdays = fields.Boolean(default=True)
    birthday_remind_days = fields.Integer()
