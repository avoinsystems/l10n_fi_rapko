# -*- encoding: utf-8 -*-

##############################################################################
#
#    Copyright (C) 2014- Avoin.Systems (<http://avoin.systems>).
#    Copyright (C) 2014- RockIt Oy (<http://rockit.fi>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#    <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models


class FiscalPositionAccount(models.Model):
    _inherit = 'account.fiscal.position.account'

    product_type = fields.Selection(
        [
            ('service', 'Service'),
            ('goods', 'Goods')
        ],
        string='Product Type',
        required=False,
        help='The product type this rule only applies to.'
    )


class FiscalPositionTax(models.Model):
    _inherit = 'account.fiscal.position.tax'

    product_type = fields.Selection(
        [
            ('service', 'Service'),
            ('goods', 'Goods')
        ],
        string='Product Type',
        required=False,
        help='The product type this rule only applies to.'
    )


class FiscalPositionAccountTemplate(models.Model):
    _inherit = 'account.fiscal.position.account.template'

    product_type = fields.Selection(
        [
            ('service', 'Service'),
            ('goods', 'Goods')
        ],
        string='Product Type',
        required=False,
        help='The product type this rule only applies to.'
    )


class FiscalPositionTaxTemplate(models.Model):
    _inherit = 'account.fiscal.position.tax.template'

    product_type = fields.Selection(
        [
            ('service', 'Service'),
            ('goods', 'Goods')
        ],
        string='Product Type',
        required=False,
        help='The product type this rule only applies to.'
    )


class FiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    # noinspection PyMethodMayBeStatic
    def _applies_to_mapping(self, product, mapping):
        if not product or not mapping.product_type:
            return True

        if mapping.product_type == 'service' and product.type == 'service':
            return True
        elif mapping.product_type == 'goods' and product.type != 'service':
            return True

        return False

    @api.v7
    def map_account(self, cr, uid, fposition_id, account_id, context=None):
        if not fposition_id:
            return account_id
        if context is None:
            context = {}

        product_id = context.get('product', False)
        product = self.pool.get('product.product')\
            .browse(cr, uid, product_id, context) \
            if product_id else False

        for pos in fposition_id.account_ids:
            if not self._applies_to_mapping(product, pos):
                continue
            if pos.account_src_id.id == account_id:
                account_id = pos.account_dest_id.id
                break
        return account_id

    @api.v8
    def map_account(self, account):
        product_id = self.env.context.get('product', False)
        product = self.env['product.product'].browse(product_id) \
            if product_id else False

        for pos in self.account_ids:
            if not self._applies_to_mapping(product, pos):
                continue
            if pos.account_src_id == account:
                return pos.account_dest_id
        return account

    @api.v7
    def map_tax(self, cr, uid, fposition_id, taxes, context=None):
        if not taxes:
            return []
        if not fposition_id:
            return map(lambda x: x.id, taxes)
        if context is None:
            context = {}

        product_id = context.get('product', False)
        product = self.pool.get('product.product')\
            .browse(cr, uid, product_id, context) \
            if product_id else False

        result = set()
        for t in taxes:
            ok = False
            for tax in fposition_id.tax_ids:
                if not self._applies_to_mapping(product, tax):
                    continue
                if tax.tax_src_id.id == t.id:
                    if tax.tax_dest_id:
                        result.add(tax.tax_dest_id.id)
                    ok = True
            if not ok:
                result.add(t.id)
        return list(result)

    @api.v8
    def map_tax(self, taxes):
        result = self.env['account.tax'].browse()

        product_id = self.env.context.get('product', False)
        product = self.env['product.product'].browse(product_id) \
            if product_id else False

        for tax in taxes:
            tax_count = 0
            for t in self.tax_ids:
                if not self._applies_to_mapping(product, t):
                    continue
                if t.tax_src_id == tax:
                    tax_count += 1
                    if t.tax_dest_id:
                        result |= t.tax_dest_id
            if not tax_count:
                result |= tax
        return result


class AccountFiscalPositionTemplate(models.Model):
    _inherit = 'account.fiscal.position.template'

    country_id = fields.Many2one(
        'res.country',
        'Country',
        help="Apply when the shipping or invoicing country matches. "
             "Takes precedence over positions matching on a country group."
    )

    country_group_id = fields.Many2one(
        'res.country.group',
        'Country Group',
        help="Apply when the shipping or invoicing country is in this "
             "country group, and no position matches the country directly."
    )

    def generate_fiscal_position(self, cr, uid, chart_temp_id,
                                 tax_template_ref, acc_template_ref,
                                 company_id, context=None):
        """
        This method generate Fiscal Position, Fiscal Position Accounts
        and Fiscal Position Taxes from templates.

        :param chart_temp_id: Chart Template Id.
        :param taxes_ids: Taxes templates reference for generating
        account.fiscal.position.tax.
        :param acc_template_ref: Account templates reference for generating
        account.fiscal.position.account.
        :param company_id: company_id selected from
        wizard.multi.charts.accounts.
        :returns: True
        """
        if context is None:
            context = {}
        obj_tax_fp = self.pool.get('account.fiscal.position.tax')
        obj_ac_fp = self.pool.get('account.fiscal.position.account')
        obj_fiscal_position = self.pool.get('account.fiscal.position')
        fp_ids = self.search(cr, uid, [('chart_template_id', '=', chart_temp_id)])
        for position in self.browse(cr, uid, fp_ids, context=context):
            fp_values = {
                'company_id': company_id,
                'name': position.name,
                'note': position.note,
            }
            if position.country_id:
                fp_values['country_id'] = position.country_id.id
            if position.country_group_id:
                fp_values['country_group_id'] = position.country_group_id.id

            new_fp = obj_fiscal_position.create(cr, uid, fp_values)
            for tax in position.tax_ids:
                obj_tax_fp.create(cr, uid, {
                    'tax_src_id': tax_template_ref[tax.tax_src_id.id],
                    'tax_dest_id': tax.tax_dest_id and tax_template_ref[tax.tax_dest_id.id] or False,
                    'position_id': new_fp,
                    'product_type': tax.product_type
                })
            for acc in position.account_ids:
                obj_ac_fp.create(cr, uid, {
                    'account_src_id': acc_template_ref[acc.account_src_id.id],
                    'account_dest_id': acc_template_ref[acc.account_dest_id.id],
                    'position_id': new_fp,
                    'product_type': acc.product_type
                })
        return True
