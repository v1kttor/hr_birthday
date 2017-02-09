# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta


def employee_birthdate(employee):
    r = datetime.strptime(employee.birthday, '%Y-%m-%d')
    return (r.month, r.day)


class HrEmployee(models.Model):
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


class HrBirthday(models.Model):
    _name = 'hr.birthday'
    _inherit = ['mail.thread']
    _description = 'Birthday Event'
    _order = 'birthday_date'

    birthday_employee = fields.Many2one(
        'hr.employee', string="Birthday Employee", required=True)
    birthday_date = fields.Date(required=True) # required=True
    department_id = fields.Many2one('hr.department', string="Department")
    celebration_date = fields.Datetime(track_visibility=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()


    def name_get(self):
        result = []
        for hrbirthday in self:
            if hrbirthday.birthday_employee.birthday == False and hrbirthday.birthday_date == False:
                name = hrbirthday.birthday_employee.name
                result.append((hrbirthday.id, name))
            else:
                name = hrbirthday.birthday_employee.name + ' ' + hrbirthday.birthday_date
                result.append((hrbirthday.id, name))
        return result


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
