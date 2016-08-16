# -*- encoding: utf-8 -*-

from lxml import etree
import copy


def parse_rec(rec):
    print(rec.tag + ' ' + rec.get('id'))
    tags = set()
    for field in rec.findall('field'):
        name = field.get('name')
        if name == 'amount':
            field.text = str(float(field.text)*100.0)
        elif name == 'type':
            field.set('name', 'amount_type')
            if field.text == 'none':
                field.text = 'fixed'
                amount = etree.Element('field', attrib={'name': 'amount'})
                amount.text = '0'
                rec.insert(-1, amount)
            elif field.text == 'balance':
                field.text = 'division'
        elif name == 'account_collected_id':
            field.set('name', 'account_id')
        elif name == 'account_paid_id':
            field.set('name', 'refund_id')
        elif name in ['base_code_id', 'tax_code_id', 'ref_tax_code_id', 'ref_base_code_id']:
            tags.add(field.get('ref'))
            rec.remove(field)
            # Todo: use tags (or something else?)

    has_amount = False
    for field in rec.findall('field'):
        if field.get('name') == 'amount':
            has_amount = True
            break
    if not has_amount:
        amount = etree.Element('field', attrib={'name': 'amount'})
        amount.text = '0'
        rec.insert(-1, amount)
    '''
    <field name="tag_ids" eval="[(6,0,[ref('account.account_tag_operating')])]"/>
    '''
    if tags:
        eval_str = u"[(6,0,["
        for tag in tags:
            eval_str += u"ref('" + tag + u"'),"
        eval_str = eval_str[:-1]  # Remove last comma
        eval_str += u"])]"
        f_tags = etree.Element('field')
        f_tags.set('name', 'tag_ids')
        f_tags.set('eval', eval_str)
        rec.insert(-1, f_tags)


def parse_tax():
    src = 'taxes.xml'
    dst = 'new_taxes.xml'
    tree = etree.parse(open(src, 'r'))
    for rec in tree.find('data').findall('record'):
        parse_rec(rec)
    tree.write(open(dst, 'w'))


def parse_code_rec(rec):
    print(rec.tag + ' ' + rec.get('model') + ' ' + rec.get('id'))
    rec.set('model', 'account.account.tag')
    f_name = etree.Element('field')
    f_name.set('name', 'name')
    f_name.text = ''
    f_applicability = etree.Element('field')
    f_applicability.set('name', 'applicability')
    f_applicability.text = 'taxes'
    for field in rec.findall('field'):
        name = field.get('name')
        if name == 'name':
            f_name.text = f_name.text + field.text
        elif name == 'code':
            f_name.text = field.text + ': ' + f_name.text
        rec.remove(field)
    rec.insert(-1, f_name)
    rec.insert(-1, f_applicability)


def parse_code():
    src = 'tax_codes.xml'
    dst = 'tax_tags.xml'
    tree = etree.parse(open(src, 'r'))
    for rec in tree.find('data').findall('record'):
        parse_code_rec(rec)
    tree.write(open(dst, 'w'))

if __name__ == '__main__':
    parse_code()
    parse_tax()
