# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from datetime import datetime
import locale
import pytz
from openerp.tools.translate import _
import time

class mcheck(osv.Model):
	_name='mcheck.mcheck'
	def create(self, cr, uid, values, context=None):
		seq_obj = self.pool.get('ir.sequence')
		name = "/"
		journal_obj = self.pool.get('account.journal')
		diario = journal_obj.browse(cr,uid,values['journal_id'],context=context)
		print diario.sequence_id
		if diario.sequence_id:
			if not diario.sequence_id.active:
				raise osv.except_osv(_('Configuration Error !'),_('Please activate the sequence of selected journal !'))
			c = dict(context)
			name = seq_obj.next_by_id(cr, uid, diario.sequence_id.id, context=c)
		values['number']=name
		b =super(mcheck, self).create(cr, uid, values, context=context)	
		return b

	def action_validate(self, cr, uid, ids, context=None):
		print ids
		for mcheck in self.browse(cr,uid,ids,context=context):
			if len(mcheck.mcheck_ids) > 0:
				total=0
				for lines in mcheck.mcheck_ids:
					total+=lines.amount
				if total > 0:
					lines_array=[]
					name = "/"
					if mcheck.number:
						name=mcheck.number
					amove_obj= self.pool.get('account.move')
					amovedata={}
					amovedata['journal_id']=mcheck.journal_id.id
					amovedata['name']=name
					amovedata['ref']=name					
					seq_obj = self.pool.get('ir.sequence')

					move_id= amove_obj.create(cr,uid,amovedata)
					mline_obj= self.pool.get('account.move.line')
					for lines in mcheck.mcheck_ids:
						lines_col={}
						lines_col['move_id']=move_id
						lines_col['name']=lines.name  or '/'
						lines_col['credit']=0
						lines_col['debit']=lines.amount
						lines_col['move_id']=move_id
						lines_col['date']=mcheck.date
						lines_col['account_id']=lines.account_id.id
						lines_col['mcheck_id']=mcheck.id
						lines_array.append(lines_col)

				

					mline_data={}
					mline_data['move_id']=move_id
					mline_data['name']= name
					mline_data['credit']=total
					mline_data['debit']=0
					mline_data['date']=mcheck.date
					mline_data['account_id']=mcheck.journal_id.default_credit_account_id.id
					mline_data['mcheck_id']=mcheck.id
					print mcheck.journal_id.default_credit_account_id.id
					line_id= mline_obj.create(cr,uid,mline_data)
					for lines2 in lines_array:
						mline_obj.create(cr,uid,lines2)
					return self.write(cr, uid, ids, {'state':'posted','number':name}, context=context)
				else:
					raise osv.except_osv(_('amount total is 0'),_("the value of total is 0") )
			else:
				raise osv.except_osv(_('No lines'),_("select more than one line") )
		
			
	_columns={
	                'journal_id':fields.many2one('account.journal', 'Journal',required=True ),
		'name':fields.char('Memo', readonly=True, ),
		'date':fields.date('Date',  select=True, 
                           help="Effective date for accounting entries", ),
		'amount': fields.float('Total', digits_compute=dp.get_precision('Account'),),
		'tax_amount':fields.float('Tax Amount', digits_compute=dp.get_precision('Account'), ),
		'reference': fields.char('Ref #', readonly=True,
		                         help="Transaction reference number.", copy=False),
		'number': fields.char('Number'),
        	'type':fields.selection([
			('sale','Sale'),
			('purchase','Purchase'),
			('payment','Payment'),
			('receipt','Receipt'),
			],'Default Type', ),		
		'mcheck_ids' :fields.one2many('mcheck.mcheck_name','mcheck_id',string="checks lines"),
		'move_ids' :fields.one2many('account.move.line','mcheck_id',string="checks lines"),
		'state':fields.selection(
		    [('draft','Draft'),
		     ('cancel','Cancelled'),
		     ('proforma','Pro-forma'),
		     ('posted','Posted')
		    ], 'Status', 
		    help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Voucher. \
		                \n* The \'Pro-forma\' when voucher is in Pro-forma status,voucher does not have an voucher number. \
		                \n* The \'Posted\' status is used when user create voucher,a voucher number is generated and voucher entries are created in account \
		                \n* The \'Cancelled\' status is used when user cancel voucher.'),


	}
	_defaults = {
	'state' : 'draft',
	'type' : 'payment',
 	'date': lambda *a: time.strftime('%Y-%m-%d'),
		} 

class mcheck_name(osv.Model):
	_name='mcheck.mcheck_name'
	_columns = {
		'mcheck_id':fields.many2one('mcheck.mcheck','mcheck'),
	        'account_id':fields.many2one('account.account','Account',domain=[('type','not in',['view'])],required=True),
		'name':fields.char('Description',),
		'amount':fields.float('Amount', digits_compute=dp.get_precision('Account')),	
        	'type':fields.selection([('dr','Debit'),('cr','Credit')], 'Dr/Cr'),
}

	_defaults = {
	'type' : 'dr',
		} 
class account_move_line(osv.osv):
	_inherit = 'account.move.line'
	_columns = {
		'mcheck_id':fields.many2one('mcheck.mcheck','mcheck'),
		}
