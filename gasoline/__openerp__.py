# -*- coding: utf-8 -*-
{	
	'name' : 'Gasoline Control',
	'author': 'Grupo Innova',
	'category': 'sale',
	'summary': 'sales, ',
	'description': """Control de Gasolina""",
	'data':[	
			'data/report_paperformat.xml',
			'views/gasoline_view.xml' ,
			'views/reporte1.xml' ,
			'views/layouts.xml' ,
			'views/gasoline_report1.xml'
	],
	'update_xml' : [
			'security/groups.xml',
			'security/ir.model.access.csv',
	],
	'depends': ['base','sale','hr','point_of_sale'],
    	'installable': True,
}
