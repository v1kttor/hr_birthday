# -*- coding: utf-8 -*-

from odoo.tests import common


class TestFollowers(common.TransactionCase):

    def test_find_followers_simple(self):
        employee = self.env['hr.employee'].create({
            'name': 'Jonas Jonaitis'})
        self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee.id,
        })
        followers = self.env['hr.birthday']._get_followers(employee)
        self.assertNotIn(employee, followers)

    def test_find_followers_manager_birthday(self):
        hr = self.env['hr.employee']
        employee1 = hr.create({
            'name': 'Jonas Jonaitis'})
        employee2 = hr.create({
            'name': 'Kazys Binkis'})
        employee3 = hr.create({
            'name': 'Raktas Raktuotas'})
        self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee2.id,
        })
        l = [employee1, employee3]
        followers = self.env['hr.birthday']._get_followers(employee2)
        self.assertNotIn(followers, l)

    def test_find_followers_employees(self):
        hr = self.env['hr.employee']
        employee1 = hr.create({
            'name': 'Jonas Jonaitis'})
        employee2 = hr.create({
            'name': 'Kazys Binkis'})
        employee3 = hr.create({
            'name': 'Raktas Raktuotas'})
        employee4 = hr.create({
            'name': 'Pelius Klaviaturius'})
        self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee2.id})
        l = [employee2, employee3, employee4]
        followers = self.env['hr.birthday']._get_followers(employee1)
        self.assertNotIn(followers, l)
'#(6, _, ids) nepanaudojau'
