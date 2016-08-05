# -*- encoding: utf-8 -*-

from lxml import etree
import copy

# user_type_id conversion dict
type_map = {
    'account.data_account_type_expense': 'account.data_account_type_expenses',
    'account.data_account_type_receivable': 'account.data_account_type_receivable',
    'account.data_account_type_asset': 'account.data_account_type_current_assets',
    'account.conf_account_type_equity': 'account.data_account_type_equity',
    'account.data_account_type_income': 'account.data_account_type_revenue',
    'account.data_account_type_bank': 'account.data_account_type_liquidity',
    'account.data_account_type_payable': 'account.data_account_type_payable',
}


def parse_record(rec):
    # Todo: views -> tags

    f_name = None
    f_code = None
    f_user_type_id = None

    for field in rec.findall('field'):
        if field.get('name') == 'type' and field.text == 'view':
            return None
    for field in rec.findall('field'):
        name = field.get('name')
        if name == 'name':
            f_name = field
        elif name == 'code':
            f_code = field
        elif name == 'user_type':
            f_user_type_id = copy.deepcopy(field)
            f_user_type_id.attrib['name'] = 'user_type_id'
            f_user_type_id.attrib['ref'] = type_map[field.attrib['ref']]
    new_rec = etree.Element(rec.tag, attrib=rec.attrib)
    new_rec.insert(-1, f_name)
    new_rec.insert(-1, f_code)
    new_rec.insert(-1, f_user_type_id)
    return new_rec


def print_record(rec):
    print(rec.tag + ' ' + rec.get('id'))
    for field in rec.findall('field'):
        name = field.get('name')
        s = '\t' + field.tag + '\t' + name + '\t'
        if name in ['name', 'code', 'type']:
            s += field.text
        elif name in ['user_type', 'parent_id']:
            s += field.get('ref')
        print(s)


def parse():
    src = 'accounts.xml'
    dst = 'new_accounts.xml'
    tree = etree.parse(open(src, 'r'))
    data = tree.find('data')
    recs = data.findall('record')
    new_data = etree.Element(data.tag, attrib=data.attrib)
    for rec in recs:
        print_record(rec)
        new_rec = parse_record(rec)
        if new_rec:
            new_data.insert(-1, new_rec)
    new_root = etree.Element('openerp')
    new_root.insert(-1, new_data)
    new_etree = etree.ElementTree(element=new_root)
    new_etree.write(open(dst, 'w'))


parse()
