# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta


"""#class hrbirthday(models.Model):
    _name = 'hrbirhtday.hrbirthday'

    name = fields.Char()
    value = fields.Integer()
   value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100
"""
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

    birthday_employee = fields.Many2one(
        'hr.employee', string="Birthday Employee", track_visibility=True)
    birthday_date = fields.Date(track_visibility=True)
    department_id = fields.Many2one('hr.department', string="Department")
    celebration_date = fields.Datetime()
    active = fields.Boolean(default=True)


class Department(models.Model):
    _inherit = 'hr.department'

    check_birthdays = fields.Boolean(default=True)
    birthday_remind_days = fields.Integer(default=7)

    def _cron_check_birthdays(self):
        today = date.today()
        departments = self.search([('check_birthdays', '=', True)])
        birthday_obj = self.env['hr.birthday']

        for department in departments:
            remind_days = timedelta(days=department.birthday_remind_days)
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
                    event = birthday_obj.create(event_vals)
                    followers = department.member_ids - member
                    followers = followers.filtered('user_id')
                    f = []
                    for follower in followers:
                        f.append(follower.user_id.partner_id.id)
                    event.message_subscribe(partner_ids=f)

                    #event.message_post(partner_ids=f.email)
                    birthday_template = self.env['mail.template']
                    inform.message_post(partner_ids=f.email)
                    inform = birthday_template.send_mail(force_send=True)

                    # templatas yra , bet nebekuria gimtadieniu artejanciu.

                    # tik reikia kad inform paruostu ir siustu mailus

# Module should have tests with at least 80% code coverage (coverage is optional).
