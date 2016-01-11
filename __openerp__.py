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

# noinspection PyStatementEffect
{
    "name": "Finland - Accounting (Raportointikoodisto)",
    "category": "Localization/Account Charts",
    "version": "1.0.2",
    "license": "AGPL-3",
    "description": """
    Finnish chart of accounts and value added taxes.

    Standard Business Reporting (=SBR or Raportointikoodisto) is a standard code set
    making Finnish official reporting easier by supplementing the common chart of accounts.

    Raportointikoodisto details: http://www.raportointikoodisto.fi/

    Finnish regulations for accounting: http://www.finlex.fi/fi/laki/ajantasa/1997/19971339
    """,
    "author": "RockIt Oy & Avoin.Systems",
    "website": "https://github.com/avoinsystems/l10n_fi_rapko",
    "depends": [
        "account",
        "account_chart",
    ],
    "data": [
        "data/tax_codes.xml",
        "data/accounts.xml",
        "data/chart_of_accounts.xml",
        "data/taxes.xml",
        "data/fiscal_positions.xml",
        "views/fiscal_position.xml",
        "views/invoice.xml",
    ],
    "active": False,
    "installable": True,
}
