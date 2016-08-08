# -*- encoding: utf-8 -*-

from lxml import etree
import copy


def parse_rec(rec):
    print(rec.tag + ' ' + rec.get('id'))
    for field in rec.findall('field'):
        name = field.get('name')
        if name == 'type':
            field.set('name', 'amount_type')
            if field.text == 'none':
                field.text = 'fixed'
                amount = etree.Element('field', attrib={'name': 'amount'})
                amount.text = '0'
                rec.insert(-1, amount)
            elif field.text == 'balance':
                field.text = 'division'
        elif name == 'account_collected_id':
            rec.remove(field)
        elif name == 'account_paid_id':
            field.set('name', 'account_id')
        elif name in ['base_code_id', 'tax_code_id', 'ref_tax_code_id', 'ref_base_code_id']:
            rec.remove(field)
            # Todo: use tags
    has_amount = False
    for field in rec.findall('field'):
        if field.get('name') == 'amount':
            has_amount = True
            break
    if not has_amount:
        amount = etree.Element('field', attrib={'name': 'amount'})
        amount.text = 'fixme'
        rec.insert(-1, amount)


def parse():
    src = 'taxes.xml'
    dst = 'new_taxes.xml'
    tree = etree.parse(open(src, 'r'))
    for rec in tree.find('data').findall('record'):
        parse_rec(rec)
    tree.write(open(dst, 'w'))


if __name__ == '__main__':
    parse()
