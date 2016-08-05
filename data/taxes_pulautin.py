# -*- encoding: utf-8 -*-

from lxml import etree
import copy


def parse_rec(rec):
    print(rec.tag + ' ' + rec.get('id'))
    for field in rec.findall('field'):
        name = field.get('name')
        if name == 'type':
            field.set('name', 'amount_type')
        elif name == 'account_collected_id':
            rec.remove(field)
        elif name == 'account_paid_id':
            field.set('name', 'account_id')
        elif name in ['base_code_id', 'tax_code_id', 'ref_tax_code_id', 'ref_base_code_id']:
            rec.remove(field)
            # Todo: use tags


def parse():
    src = 'taxes.xml'
    dst = 'new_taxes.xml'
    tree = etree.parse(open(src, 'r'))
    for rec in tree.find('data').findall('record'):
        parse_rec(rec)
    tree.write(open(dst, 'w'))


if __name__ == '__main__':
    parse()
