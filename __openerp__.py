# -*- coding: utf-8 -*-
{
    'name': 'MonoCNAB',
    'version': '1.0',
    'category': 'Tools',
    'description': '',
    'author': 'Monocon',
    'website': 'http://monocon.com.br',
    'summary': 'CNAB',
    'depends': [
        'base',
        'account',
        'l10n_br_account',
    ],
    'data': [
        'cnab_view.xml',
        'cnab_workflow.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

