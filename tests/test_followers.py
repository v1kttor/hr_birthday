# -*- coding: utf-8 -*-

from odoo.tests import common


class TestFollowers(common.TransactionCase):

    def test_find_followers_simple(self):
        employee = self.env['hr.employee'].create({
            'name': 'Jonas Jonaitis'})
        dp = self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee.id,
        })
        followers = self.env['hr.birthday']._get_followers(dp, employee)
        self.assertNotIn(employee, followers)

    def test_find_followers_manager_birthday(self):
        hr = self.env['hr.employee']
        employee1 = hr.create({
            'name': 'Jonas Jonaitis'})
        employee2 = hr.create({
            'name': 'Kazys Binkis'})
        employee3 = hr.create({
            'name': 'Raktas Raktuotas'})
        employees = [employee1.id, employee2.id, employee3.id]
        dp = self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee2.id,
            'member_ids': [(6, 0, employees)],
        })
        followers = self.env['hr.birthday']._get_followers(dp, employee2)
        self.assertNotIn(employee2, followers)
        self.assertIn(employee1, followers)
        self.assertIn(employee3, followers)

    def test_find_followers_employees(self):
        hr = self.env['hr.employee']
        employee1 = hr.create({
            'name': 'Jonas Jonaitis'})
        employee2 = hr.create({
            'name': 'Kazys Binkis'})
        employee3 = hr.create({
            'name': 'Raktas Raktuotas'})
        l = [employee1.id, employee2.id]
        dp = self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee3.id,
            'member_ids': [(6, 0, l)],
        })
        followers = self.env['hr.birthday']._get_followers(dp, employee1)
        self.assertIn(employee2, followers)
        self.assertIn(employee3, followers)

    def test_find_followers_manager_not_employee(self):
        hr = self.env['hr.employee']
        employee1 = hr.create({
            'name': 'Jonas Jonaitis'})
        employee2 = hr.create({
            'name': 'Kazys Binkis'})
        employee3 = hr.create({
            'name': 'Raktas Raktuotas'})
        employees = [employee1.id, employee3.id]
        department = self.env['hr.department'].create({
            'name': 'fake_department',
            'manager_id': employee2.id,
            'member_ids': [(6, 0, employees)],
        })
        followers = self.env['hr.birthday']._get_followers(
            department, employee1)
        self.assertNotIn(employee1, followers)
        self.assertIn(employee2, followers)
        self.assertIn(employee3, followers)
