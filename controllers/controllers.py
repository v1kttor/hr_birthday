# -*- coding: utf-8 -*-
from odoo import http

# class HrBirthday(http.Controller):
#     @http.route('/hr_birthday/hr_birthday/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_birthday/hr_birthday/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_birthday.listing', {
#             'root': '/hr_birthday/hr_birthday',
#             'objects': http.request.env['hr_birthday.hr_birthday'].search([]),
#         })

#     @http.route('/hr_birthday/hr_birthday/objects/<model("hr_birthday.hr_birthday"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_birthday.object', {
#             'object': obj
#         })