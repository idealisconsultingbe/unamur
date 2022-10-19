{
    'name': "U-namur website",
    'version': '1.0.0',
    'summary': """
        University of Namur Website Module """,

    'description': """
         This module contains customization on the website module. 
    """,
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'category': 'website',
    'depends': ['account', 'base', 'website', 'hr_expense', 'sale_expense', 'portal', 'purchase', 'sale'],

    'data': [
        # Data
        'data/expense_data.xml',
        # Views
        'views/expense_templates.xml',

    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
