# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


def employee_birthdate(employee):
    r = datetime.strptime(
        employee.birthday, DEFAULT_SERVER_DATE_FORMAT)
    return (r.month, r.day)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def get_upcoming_birthday_date(self, delta_days, today_date=None):
        self.ensure_one()
        zero = timedelta()
        delta = timedelta(days=delta_days)
        if today_date is None:
            today_date = date.today()
        if not self.birthday:
            return
        birthday = datetime.strptime(
            self.birthday, DEFAULT_SERVER_DATE_FORMAT).replace(
            year=today_date.year).date()
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
        'hr.employee', string='Birthday Employee', required=True)
    birthday_date = fields.Date(required=True)
    department_id = fields.Many2one('hr.department', string='Department')
    celebration_date = fields.Datetime(track_visibility=True)
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for birthday in self:
            if not birthday.birthday_date:
                name = birthday.birthday_employee.name
                result.append((birthday.id, name))
            else:
                name = ('%s %s') % (
                    birthday.birthday_employee.name,
                    birthday.birthday_date)
                result.append((birthday.id, name))
        return result

    @api.model
    def find_old_birthdays(self, today_date=None, days_to_false=14):
        if today_date is None:
            today_date = date.today()
        days_to_false = timedelta(days=days_to_false)
        return self.search([
            ('active', '=', True),
            ('birthday_date', '!=', False),
            ('birthday_date', '<', today_date - days_to_false)
        ])

    @api.model
    def _cron_check_old_birthdays_events(self, days_to_false=14):
        for birthday in self.find_old_birthdays(days_to_false=days_to_false):
            birthday.active = False


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    check_birthdays = fields.Boolean(default=True)
    birthday_remind_days = fields.Integer(
        default=7,
        help="How many days before the birthday should everybody be reminded")

    def _cron_check_birthdays(self):
        departments = self.search([('check_birthdays', '=', True)])
        birthday_obj = self.env['hr.birthday']

        for department in departments:
            for member in department.member_ids.filtered('birthday'):
                member_birthday = member.get_upcoming_birthday_date(
                    department.birthday_remind_days)

                if not member_birthday:
                    continue
                events = birthday_obj.search([
                    ('birthday_employee', '=', member.id),
                    ('birthday_date', '=', member_birthday),
                ])
                if events:
                    continue
                event_vals = {
                    'birthday_employee': member.id,
                    'birthday_date': member_birthday,
                    'department_id': department.id,
                }
                event = birthday_obj.create(event_vals)
                followers = department.member_ids - member
                followers = followers.filtered('user_id', 'manager_id')
                f = []
                for follower in followers:
                    f.append(
                        follower.user_id.partner_id.id).mapped(
                        event.message_subscribe(partner_ids=f))
                template = self.env.ref(
                    'hr_birthday.email_template_birthday')
                event.message_post_with_template(template.id)
