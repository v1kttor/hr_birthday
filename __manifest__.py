# -*- coding: utf-8 -*-
{
    'name': "Birthdays",

    'summary': """Birthdays module which reminds us about our colleagues
    upcoming birthday. Module only informs us about our department
    colleagues birthdays, so we will not know about other departments.
    Also, module lets the user print report which will show all
    department employees
    birthdays. Also, there is a feature which marks birthday events
    t false if they are older than two weeks.""",
    'description': "",
    'author': "Viktoras",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'HR',
    'version': '10.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hr_birthday.xml',
        'views/reports.xml',
        'data/ir.xml',
        'data/optional.xml',
        'views/hr.xml',
        'views/mail.xml',
    ],
}
