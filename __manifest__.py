# -*- coding: utf-8 -*-
{
    'name': "Birthdays module",

    'summary': """Birthdays reminder""",

    'description': """
        Very very very long description of module's purpose
    """,

    'author': "hbee",
    'website': "http://www.hbee.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv', # nors dar reiktu patvarkyt pagal hive uzduoti . daugiau pagooglint
        #'views/views.xml',
        #'views/templates.xml',
        'security/security.xml',
        'views/reports.xml',
        'data/ir.xml',
        'views/hr.xml',
        'views/mail.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
