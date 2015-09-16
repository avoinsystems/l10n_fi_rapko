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

    apply_domain = fields.Char(
        'Apply'
    )


class FiscalPositionTax(models.Model):
    _inherit = 'account.fiscal.position.tax'


class FiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.v7
    def map_account(self, cr, uid, fposition_id, account_id, context=None):
        if not fposition_id:
            return account_id
        for pos in fposition_id.account_ids:
            if pos.account_src_id.id == account_id:
                account_id = pos.account_dest_id.id
                break
        return account_id

    @api.v8
    def map_account(self, account):
        product_id = self.env.context.get('product', False)
        if product_id:
            product = self.env['product.product'].browse(product_id)

        for pos in self.account_ids:
            if pos.account_src_id == account:
                return pos.account_dest_id
        return account

    @api.v7
    def map_tax(self, cr, uid, fposition_id, taxes, context=None):
        if not taxes:
            return []
        if not fposition_id:
            return map(lambda x: x.id, taxes)
        result = set()
        for t in taxes:
            ok = False
            for tax in fposition_id.tax_ids:
                if tax.tax_src_id.id == t.id:
                    if tax.tax_dest_id:
                        result.add(tax.tax_dest_id.id)
                    ok=True
            if not ok:
                result.add(t.id)
        return list(result)

    @api.v8
    def map_tax(self, taxes):
        result = self.env['account.tax'].browse()
        for tax in taxes:
            tax_count = 0
            for t in self.tax_ids:
                if t.tax_src_id == tax:
                    tax_count += 1
                    if t.tax_dest_id:
                        result |= t.tax_dest_id
            if not tax_count:
                result |= tax
        return result
