# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)
grey = "\x1b[38;21m"
yellow = "\x1b[33;21m"
red = "\x1b[31;21m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
green = "\x1b[32m"
blue = "\x1b[34m"
# Ahmed Salama Code Start ---->
_STATES = [('draft', 'Draft'),
           ('confirmed', 'Confirm'),
           ('approved', 'Mang. Approved'),
           ('done', 'Final Approved'),
           ('cancel', 'Cancel')]


# Ahmed Salama Code Start ---->


class HrEmployeeexcuse(models.Model):
	_name = 'hr.employee.excuse'
	_description = "HR Employee Excuse"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_check_company_auto = True
	
	@api.model
	def _get_employee_id_domain(self):
		res = [('id', '=', 0)]  # Nothing accepted by domain, by default
		if self.user_has_groups('hr.group_hr_manager'):
			res = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]"  # Then, domain accepts everything
		elif self.env.user.employee_ids:
			employee = self.env.user.employee_id
			res = [
				'|', '|',
				('department_id.manager_id', '=', employee.id),
				('parent_id', '=', employee.id),
				('id', '=', employee.id),
				'|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id),
			]
		elif self.env.user.employee_id:
			employee = self.env.user.employee_id
			res = [('id', '=', employee.id), '|', ('company_id', '=', False),
			       ('company_id', '=', employee.company_id.id)]
		return res
	
	# Main Details
	name = fields.Char(default="/", readonly=1)
	company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
	                             index=True, required=True, readonly=1,
	                             states={'draft': [('readonly', False)]})
	active = fields.Boolean(default=True)
	state = fields.Selection(_STATES, "State", default='draft', tracking=True)
	# Employee Details
	employee_id = fields.Many2one('hr.employee', "Employee", required=True, readonly=1,
	                              states={'draft': [('readonly', False)]}, tracking=True,
	                              default=lambda self: self.env.user.employee_id,
	                              domain=lambda self: self._get_employee_id_domain(), check_company=True)
	identification_id = fields.Char(string='Identification No', tracking=True)
	department_id = fields.Many2one('hr.department', 'Department', tracking=True,
	                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	job_id = fields.Many2one('hr.job', 'Job Position', tracking=True,
	                         domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	
	# excuse Details
	type_id = fields.Many2one('hr.employee.excuse.type', "Excuse Type",
	                          required=True, ondelete='cascade', tracking=True)
	date_start = fields.Datetime("Start Date", default=fields.Datetime.now(), readonly=1,
	                             states={'draft': [('readonly', False)]}, tracking=True, required=True)
	date_end = fields.Datetime("End Date", readonly=1,
	                           states={'draft': [('readonly', False)]}, tracking=True, required=True)
	excuse_details = fields.Text("excuse Details", tracking=True, required=True)
	
	def _comp_show_approve_button(self):
		"""
		Show Approve button only if this employee on logged-in user employees OR this issuer is employee manager
		"""
		for rec in self:
			show_approve_button = False
			if rec.employee_id in self.env.user.employee_id.child_ids \
					or rec.employee_id.department_id.manager_id == self.env.user.employee_id \
					or self.user_has_groups('hr.group_hr_manager'):
				show_approve_button = True
			rec.show_approve_button = show_approve_button
			
	show_approve_button = fields.Boolean(compute=_comp_show_approve_button)
	
	# --------------------------------------------------
	# CRUD
	# --------------------------------------------------
	
	@api.model
	def create(self, vals):
		"""
		Add Seq for excuse
		:param vals: create vals
		:return: SUPER
		"""
		vals['name'] = self.env['ir.sequence'].sudo().next_by_code('hr.employee.excuse.code')
		attend = super(HrEmployeeexcuse, self).create(vals)
		return attend
	
	@api.model
	def default_get(self, fields):
		"""
		Load default employee on open for create
		:param fields: default dict
		:return: SUPER
		"""
		defaults = super(HrEmployeeexcuse, self).default_get(fields)
		if not defaults.get('employee_id'):
			employee_id = self.env.user.employee_id
			if not employee_id:
				raise Warning(
					_("Current user:%s ]\n have no related employee!!!, please check it first" % self.env.user.name))
			defaults['employee_id'] = employee_id.id
		employee_id = self.env['hr.employee'].browse(defaults.get('employee_id'))
		# Collect Employee details
		defaults['department_id'] = employee_id.department_id and employee_id.department_id.id or False
		defaults['job_id'] = employee_id.job_id and employee_id.job_id.id or False
		defaults['identification_id'] = employee_id.identification_id
		return defaults
	
	# --------------------------------------------------
	# Actions
	# --------------------------------------------------
	
	def action_confirm(self):
		"""
		- Confirm Details
		"""
		for rec in self:
			rec.state = 'confirmed'
	
	def action_approve(self):
		"""
		- Direct manger approved sheet
		"""
		for rec in self:
			rec.state = 'approved'
	
	def action_done(self):
		"""
		- Hr manger Final approve sheet
		"""
		for rec in self:
			rec.state = 'done'
	
	def action_cancel(self):
		"""
		- Cancel excuse
		"""
		for rec in self:
			rec.state = 'cancel'
	
	def action_draft(self):
		"""
		- reset state to draft
		"""
		for rec in self:
			rec.state = 'draft'
	
	# --------------------------------------------------
	# Business methods
	# --------------------------------------------------
	
	@api.onchange('employee_id')
	def onchange_employee_id(self):
		"""
		Get Default Employee Details
		:return:
		"""
		self.department_id = self.employee_id.department_id and self.employee_id.department_id.id or False
		self.job_id = self.employee_id.job_id and self.employee_id.job_id.id or False
		self.identification_id = self.employee_id.identification_id

	def export_records_pdf(self):
		return self.env.ref('hr_employee_excuses.action_hr_employee_excuses').report_action(self.ids)

# Ahmed Salama Code End.
