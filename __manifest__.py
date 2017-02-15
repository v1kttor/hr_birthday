# -*- coding: utf-8 -*-
{
    'name': "Birthdays",

    'summary': """Birthdays module which remind
     us about our colleagues upcoming birthday""",

    'description': """

    """,

    'author': "Viktoras",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'HR',
    'version': '0.1',

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
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
