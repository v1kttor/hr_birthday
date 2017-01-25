# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from datetime import timedelta


#class hrbirthday(models.Model):
#    _name = 'hrbirhtday.hrbirthday'

#    name = fields.Char()
#    value = fields.Integer()
#    value2 = fields.Float(compute="_value_pc", store=True)
#    description = fields.Text()

#    @api.depends('value')
#    def _value_pc(self):
#        self.value2 = float(self.value) / 100


class Birthday(models.Model):
    _name = 'hr.birthday'
    _inherit = ['mail.thread']

    birthday_employee = fields.Many2one('hr.employee')
    birthday_date = fields.Date()
    department_id = fields.Many2one('hr.department')
    celebration_date = fields.Datetime()
    active = fields.Boolean(default=True)


class Department(models.Model):
    _inherit = 'hr.department'

    check_birthdays = fields.Boolean(default=True)
    birthday_remind_days = fields.Integer()

    def _cron_check_birthdays(self):
        if check_birthdays == True and birthday_remind_days == True:
            return True
        else:
            pass # create event


#    A Cron job runs (default interval: 2 hours) and checks each department,
# which would like to be informed on birthdays (check_birthdays == True)
# and if there are any upcoming birthdays in birthday_remind_days number
# of days.
# If there are, a birthday event (hr.birthday) record
#(if not yet exists) is created for the birthday of the employee.

#   All employees of the department (including the manager, if any)
# of the birthday boy/girl are made followers of the birthday event document.

#   Email notifications are sent to all the followers
# (except the birthday boy/girl) informing about the upcoming event.
