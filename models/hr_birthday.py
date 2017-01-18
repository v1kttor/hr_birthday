# Comments

from datetime import timedelta
from odoo import fields, models, api

class Birth(models,Model):
    _name = hr_birthday.birth

    birthday_employee = fields.Many2one(hr.employee)
    birthday_date = fields.Date()
    department_id = fields.Many2one('hr_department')
    celebration_date = fields.Datetime()
    active = fields.Boolean(default=True)
