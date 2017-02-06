# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta


def employee_birthdate(employee):
    r = datetime.strptime(employee.birthday, '%Y-%m-%d')
    return (r.month, r.day)


class HrBirthday(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def get_upcoming_birthday_date(self, delta_days, today_date=None):
        self.ensure_one()
        if today_date is None:
            today_date = date.today()
        if not self.birthday:
            return
        birthday = datetime.strptime(self.birthday, '%Y-%m-%d').date()
        birthday = birthday.replace(year=today_date.year)
        delta = timedelta(days=delta_days)
        zero = timedelta()
        diff = birthday - today_date
        if diff > zero and diff <= delta:
            return birthday

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
        departments = self.search([('check_birthdays', '=', True)])
        birthday_obj = self.env['hr.birthday']

        for department in departments:
            for member in department.member_ids.filtered('birthday'):
                member_birthday = member.get_upcoming_birthday_date(
                    department.birthday_remind_days)

                if member_birthday:
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
                        f.append(follower.user_id.partner_id.id) # prideda followerius
                    event.message_subscribe(partner_ids=f)
                    template = self.env.ref("hr_birthday.email_template_birthday")
                    event.message_post_with_template(template.id)

                    # Module should have tests with at least 80% code coverage (coverage is optional).
