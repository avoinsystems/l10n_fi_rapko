# -*- encoding: utf-8 -*-

from lxml import etree
import copy


class TaxParser:
    tax_src = 'taxes.xml'
    code_src = 'tax_codes.xml'
    tax_dst = 'new_taxes.xml'
    tag_dst = 'tax_tags.xml'

    # code_dict = {}  # Todo: not needed?
    # seq_dict = {}

    def parse_rec(self, rec):
        print(rec.tag + ' ' + rec.get('id'))
        tags = set()
        f_tax_code_id = None
        f_parent_id = None
        for field in rec.findall('field'):
            name = field.get('name')
            if name == 'amount':
                field.text = str(float(field.text) * 100.0)
            elif name == 'type':
                field.set('name', 'amount_type')
                if field.text == 'none':
                    field.text = 'fixed'
                    amount = etree.Element('field', attrib={'name': 'amount'})
                    amount.text = '0'
                    rec.insert(-1, amount)
                elif field.text == 'balance':
                    field.text = 'group'
            elif name == 'account_collected_id':
                field.set('name', 'account_id')
            elif name == 'account_paid_id':
                field.set('name', 'refund_id')
            elif name in ['base_code_id', 'tax_code_id', 'ref_tax_code_id', 'ref_base_code_id']:
                tags.add(field.get('ref') + '_tag')
                if name == 'tax_code_id':
                    f_tax_code_id = field
                rec.remove(field)
                # Todo: use tags (and/or something else?)
            elif name == 'parent_id':
                f_parent_id = field

        '''
        if f_parent_id is None and f_tax_code_id is not None:
            f_parent_id = etree.Element('field')
            f_parent_id.set('name', 'parent_id')
            f_parent_id.set('ref', f_tax_code_id.get('ref'))
            rec.insert(-1, f_parent_id)
        '''

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

    """
    def parse_code_tax(self, rec, data, insert_counter):
        # print(rec.tag + ' ' + rec.get('model') + ' ' + rec.get('id'))
        new_rec = etree.Element('record')
        new_rec.set('id', rec.get('id'))
        new_rec.set('model', 'account.tax.template')
        tax_name = None
        for field in rec.findall('field'):
            name = field.get('name')
            if name == 'code':
                if tax_name:
                    tax_name = field.text + u' ' + tax_name
                else:
                    tax_name = field.text
            elif name == 'name':
                if tax_name:
                    tax_name += u' ' + field.text
                else:
                    tax_name = field.text
            elif name == 'parent_id':
                new_rec.insert(-1, copy.deepcopy(field))
        f_name = etree.Element('field')
        f_name.set('name', 'name')
        f_name.text = tax_name
        new_rec.insert(-1, f_name)
        f_type = etree.Element('field')
        f_type.set('name', 'amount_type')
        f_type.text = 'group'
        new_rec.insert(-1, f_type)
        f_amount = etree.Element('field')
        f_amount.set('name', 'amount')
        f_amount.text = '0.0'
        new_rec.insert(-1, f_amount)
        f_sequence = etree.Element('field')
        f_sequence.set('name', 'sequence')
        f_sequence.text = '0'
        new_rec.insert(-1, f_sequence)
        f_chart = etree.Element('field')
        f_chart.set('name', 'chart_template_id')
        f_chart.set('ref', 'chart_template_fi_rapko')
        new_rec.insert(-1, f_chart)
        '''
        if self.code_dict.get(new_rec.get('id')):
            eval_str = u"[(6,0,["
            for ref in self.code_dict[new_rec.get('id')]:
                eval_str += u"ref('" + ref + u"'),"
            eval_str = eval_str[:-1]  # Remove last comma
            eval_str += u"])]"
            f_child_ids = etree.Element('field')
            f_child_ids.set('name', 'children_tax_ids')
            f_child_ids.set('eval', eval_str)
            new_rec.insert(-1, f_child_ids)
        '''
        data.insert(insert_counter, new_rec)
    """

    def print_field(self, rec, field_name):
        for field in rec.findall('field'):
            if field.get('name') == field_name:
                print(u'\t' + field.text + u'\t' + rec.get('id'))

    def get_type(self, rec):
        for field in rec.findall('field'):
            if field.get('name') == 'type_tax_use':
                return field.text
        return None

    def find_children(self, rec, data):
        r_id = rec.get('id')
        children = set()
        super_group = False
        print(rec.get('id'))
        for r in data.findall('record'):
            for field in r.findall('field'):
                name = field.get('name')
                if name == 'parent_id' and field.get('ref') == r_id:
                    children.add(r)
                    if self.get_type(r) is None:
                        super_group = True
                    self.print_field(r, 'type_tax_use')
                    break
        if super_group:
            to_remove = set()
            for child in children:
                if self.get_type(child) is not None:
                    print('Remove')
                    to_remove.add(child)
            for child in to_remove:
                children.remove(child)

        return children

    def set_children(self, rec, data):
        children = self.find_children(rec, data)
        if len(children) == 0:
            return
        eval_str = u"[(6,0,["
        for child in children:
            ref = child.get('id')
            eval_str += u"ref('" + ref + u"'),"
        eval_str = eval_str[:-1]  # Remove last comma
        eval_str += u"])]"
        f_child_ids = etree.Element('field')
        f_child_ids.set('name', 'children_tax_ids')
        f_child_ids.set('eval', eval_str)
        rec.insert(-1, f_child_ids)

    @staticmethod
    def reverse(data):
        new_data = etree.Element('data')
        for rec in data.findall('record'):
            new_data.insert(0, rec)
        return new_data

    def remove_parent_id(self, data):
        """
        Call after set_children
        """
        for rec in data.findall('record'):
            for field in rec.findall('field'):
                if field.get('name') == 'parent_id':
                    rec.remove(field)
                    break

    def check(self, data):
        for rec in data.findall('record'):
            print(rec.get('id'))
            for field in rec.findall('field'):
                name = field.get('name')
                if name in ['name', 'type_tax_use']:
                    print(u'\t' + name + u':\t' + field.text)
                elif name in ['children_tax_ids', 'tag_ids']:
                    print('\t' + field.get('eval'))

    def parse_tax(self):
        f = open(self.tax_src, 'r')
        tree = etree.parse(f)
        f.close()
        data = tree.find('data')
        print('=== Parse Records ===')
        for rec in data.findall('record'):
            self.parse_rec(rec)
        '''
        f = open(self.code_src, 'r')
        code_tree = etree.parse(f)
        f.close()
        insert_counter = 0
        for rec in code_tree.find('data').findall('record'):
            self.parse_code_tax(rec, data, insert_counter)
            insert_counter += 1
        '''
        print('=== Reverse Records ===')
        new_data = self.reverse(data)
        print('=== Set Children ===')
        for rec in new_data.findall('record'):
            self.set_children(rec, new_data)
        self.remove_parent_id(new_data)
        print('=== Check ===')
        self.check(new_data)
        new_root = etree.Element('openerp')
        new_root.insert(-1, new_data)
        new_tree = etree.ElementTree(element=new_root)
        new_tree.write(open(self.tax_dst, 'w'))

    @staticmethod
    def parse_code_tag(rec):
        # print(rec.tag + ' ' + rec.get('model') + ' ' + rec.get('id'))
        rec.set('id', rec.get('id') + '_tag')
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

    def parse_code(self):
        f = open(self.code_src, 'r')
        tree = etree.parse(f)
        f.close()
        for rec in tree.find('data').findall('record'):
            self.parse_code_tag(rec)
        tree.write(open(self.tag_dst, 'w'))


if __name__ == '__main__':
    p = TaxParser()
    # p.parse_code()
    p.parse_tax()
