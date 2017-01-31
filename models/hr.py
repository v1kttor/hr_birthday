# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta


#class hrbirthday(models.Model):
#    _name = 'hrbirhtday.hrbirthday'

#    name = fields.Char()
#    value = fields.Integer()
#    value2 = fields.Float(compute="_value_pc", store=True)
#    description = fields.Text()

#    @api.depends('value')
#    def _value_pc(self):
#        self.value2 = float(self.value) / 100

def employee_birthdate(employee):
    r = datetime.strptime(employee.birthday, '%Y-%m-%d')
    return (r.month, r.day)

class Reports(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def sort_by_birthday(self):
        return self.sorted(key=employee_birthdate)

class Birthday(models.Model):
    _name = 'hr.birthday'
    _inherit = ['mail.thread']
    _description = 'Birthday Module'
    _order = 'birthday_date desc, birthday_employee'

    birthday_employee = fields.Many2one('hr.employee', string="Birthday Employee")
    birthday_date = fields.Date()
    department_id = fields.Many2one('hr.department', string="Department")
    celebration_date = fields.Datetime()
    active = fields.Boolean(default=True)


class Department(models.Model):
    _inherit = 'hr.department'

    check_birthdays = fields.Boolean(default=True)
    birthday_remind_days = fields.Integer()

    def _cron_check_birthdays(self):
        today = date.today()
        departments = self.search([('check_birthdays', '=', True)])
        birthday_obj = self.env['hr.birthday']

        for department in departments:
            remind_days = timedelta(days=department.birthday_remind_days) # birthday_remind_days number of days
            for member in department.member_ids.filtered('birthday'):
                member_birthday = datetime.strptime(
                    member.birthday, '%Y-%m-%d').date()
                member_birthday = member_birthday.replace(year=today.year)
                difference = member_birthday - today
                if difference == remind_days:
                    events = birthday_obj.search([
                        ('birthday_employee', '=', member.id),
                        ('birthday_date', '=', member_birthday),
                    ])
                    if events:
                        continue
                    event_vals = {
                        'birthday_employee' : member.id,
                        'birthday_date' : member_birthday,
                        'department_id' : department.id,
                        'active' : True,
                        }
                    birthday_obj.create(event_vals)
                    #import pdb; pdb.set_trace()

# If there are, a birthday event (hr.birthday) record
#(if not yet exists) is created for the birthday of the employee.

#   All employees of the department (including the manager, if any)
# of the birthday boy/girl are made followers of the birthday event document.

#   Email notifications are sent to all the followers
# (except the birthday boy/girl) informing about the upcoming event.
