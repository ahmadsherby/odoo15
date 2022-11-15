# -*- coding: utf-8 -*-
{
    'name': 'HR Employee Excuse',
    'summary': 'Give Employee to submit excuse to him or to his followers',
    'version': '0.2',
    'license': "AGPL-3",
    'author': 'Telenoc, Ahmed Salama',
    'category': 'Human Resources/Employee',
    'depends': ['hr'],
    'website': 'http://www.telenoc.org',
    'data': [
        'data/hr_employee_excuse_type_data.xml',
        'data/hr_employee_excuse_data.xml',
        
        # 'security/',
        'security/ir.model.access.csv',

        'views/hr_employee_excuse_type_view.xml',
        'views/hr_employee_excuse_view.xml',
        'views/hr_employee_view_changes.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
