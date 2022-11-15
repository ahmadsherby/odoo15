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
	
	emp_excuse_ids = fields.One2many('hr.employee.excuse', 'employee_id',
	                                                         "Employee excuses")
	excuses_count = fields.Integer(compute='_compute_excuses_count', string='excuses Count')
	
	def _compute_excuses_count(self):
		# read_group as sudo, since contract count is displayed on form view
		excuse_data = self.env['hr.employee.excuse'].sudo().read_group(
			[('employee_id', 'in', self.ids)], ['employee_id'], ['employee_id'])
		result = dict((data['employee_id'][0], data['employee_id_count']) for data in excuse_data)
		for employee in self:
			employee.excuses_count = result.get(employee.id, 0)
	
	def action_open_excuses(self):
		self.ensure_one()
		action = self.env["ir.actions.actions"]._for_xml_id('hr_employee_excuses.hr_hr_employee_excuse_action')
		action['domain'] = [('employee_id', '=', self.id)]
		return action

# Ahmed Salama Code End.
