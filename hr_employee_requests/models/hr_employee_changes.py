# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
igrey = '\x1b[38;21m'
yellow = '\x1b[33;21m'
red = '\x1b[31;21m'
bold_red = '\x1b[31;1m'
reset = '\x1b[0m'
green = '\x1b[32m'
blue = '\x1b[34m'
# Ahmed Salama Code Start ---->


class HrEmployeeInherit(models.Model):
	_inherit = 'hr.employee'
	
	emp_request_ids = fields.One2many('hr.employee.request', 'employee_id',
	                                                         "Employee Requests")
	requests_count = fields.Integer(compute='_compute_requests_count', string='Requests Count')
	
	def _compute_requests_count(self):
		# read_group as sudo, since contract count is displayed on form view
		request_data = self.env['hr.employee.request'].sudo().read_group(
			[('employee_id', 'in', self.ids)], ['employee_id'], ['employee_id'])
		result = dict((data['employee_id'][0], data['employee_id_count']) for data in request_data)
		for employee in self:
			employee.requests_count = result.get(employee.id, 0)
	
	def action_open_requests(self):
		self.ensure_one()
		action = self.env["ir.actions.actions"]._for_xml_id('hr_employee_requests.hr_hr_employee_request_action')
		action['domain'] = [('employee_id', '=', self.id)]
		return action

# Ahmed Salama Code End.
