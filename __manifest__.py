# -*- coding: utf-8 -*-
{
    'name': "HR Birthday Reminder",
    'summary': """Birthdays module which reminds us about our colleagues
    upcoming birthday.""",
    'description': "Birthday reminder",
    'author': "Viktoras",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'HR',
    'version': '10.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'hr',
     ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hr_birthday.xml',
        'views/reports.xml',
        'data/ir.xml',
        'views/hr.xml',
        'views/mail.xml',
    ],
}
