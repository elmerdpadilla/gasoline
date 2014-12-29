from openerp.osv import osv
class reporte(osv.AbstractModel):
	_name = 'report.gasoline.report_closing'
	def render_html(self, cr, uid, ids, data=None, context=None):
		report_obj = self.pool['report']
		report = report_obj._get_report_from_name(cr, uid, 'gasoline.report_closing')
		docargs = {
			'doc_ids': ids,
			'doc_model': report.model,
			'docs': self.pool[report.model].browse(cr, uid, ids, context=context),
			}
		return report_obj.render(cr, uid, ids, 'gasoline.report_closing',docargs, context=context)
"""
	def __init__(self, cr, uid, name, context=None): 
		super(sale_quotation_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({'get_total': self._get_total,})
	def _get_total(self, lines, field):
		total = 0.0
		for line in lines.reading_finish :
			total += line.price_list or 0.0
		return total
"""
