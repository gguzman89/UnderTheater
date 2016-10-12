# vim: set fileencoding=utf-8 :
import ast

def convert_list_string(list_convert):
    list_element = ast.literal_eval(list_convert)
    list_len = len(list_element) - 1
    elem_string = ""
    for n, elem in enumerate(list_element):
        if list_len == n:
            elem_string += " y"
        elem_string += " %s" % elem
    return elem_string
