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
# Ahmed Salama Code Start ---->


class HrEmployeeexcuseType(models.Model):
	_name = 'hr.employee.excuse.type'
	_description = "HR Employee Excuse Type"
	_check_company_auto = True
	
	name = fields.Char("Excuse Type", required=True, translate=True)
	company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
	                             index=True, required=True)
	note = fields.Text("Note", translate=True)


# Ahmed Salama Code End.
