{
    'name': 'Lagrange Interpolation Integration',
    'version': '16.0.1.0.0',
    'category': 'Tools',
    'summary': 'Integration module for Lagrange interpolation data',
    'description': '''
        This module allows integration of Lagrange interpolation results
        from external Django application into Odoo.
        
        Features:
        - Store interpolation points
        - Store polynomial coefficients
        - Visualize interpolation results
        - Export data analysis
    ''',
    'author': 'Lagrange Animator Team',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/interpolation_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
