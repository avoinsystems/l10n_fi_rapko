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

{
    "name": "Finland - Accounting (Raportointikoodisto)",
    "version": "1.0",
    "description": """
	Finnish chart of accounts and value added taxes.

	Raportointikoodisto (Rapko) details: http://www.raportointikoodisto.fi/
        Finnish regulations for accounting: http://www.finlex.fi/fi/laki/ajantasa/1997/19971339
        """,
    "author": "RockIt Oy & Avoin.Systems",
    "website": "http://rockit.fi http://avoin.systems",
    "category": "Localization/Account Charts",
    "depends": [
        "account",
        "account_chart",
        "base_vat"
        ],
    "update_xml": [
        'l10n_fi_taxes_code.xml',
        'l10n_fi_chart_of_accounts.xml',
        'l10n_fi_taxes.xml',
        'l10n_fi_chart_wizard.xml'
        ],
    "active": False,
    "installable": True,
}
