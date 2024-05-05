# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

"""
@brief Utilities involving LOXI naming conventions

Utility functions for OpenFlow class generation

These may need to be sorted out into language specific functions
"""

import re
import sys

import loxi_globals
from generic_utils import find, memoize

##
# Class types:
#
# Virtual
#    A virtual class is one which does not have an explicit wire
#    representation.  For example, an inheritance super class
#    or a list type.
#
# List
#    A list of objects of some other type
#
# TLV16
#    The wire represenation starts with 16-bit type and length fields
#
# OXM
#    An extensible match object
#
# OXS
#    Extensible Stats Object
#
# Message
#    A top level OpenFlow message
#
#

class NoneClass(object):
    def is_instanceof(self, x):
        return False
none_item = NoneClass()

def _unified_by_name(cls):
    c = loxi_globals.unified.class_by_name(cls)
    return c if c is not None else none_item

@memoize
def class_is_message(cls):
    """
    Return True if cls is a message object based on info in unified
    """
    if cls == "of_header":
        return False
    else:
        return _unified_by_name(cls).is_instanceof("of_header")

def class_is_oxm(cls):
    """
    Return True if cls_name is an OXM object
    """
    return _unified_by_name(cls).is_instanceof("of_oxm")

def class_is_oxs(cls):
    """
    Return True if cls_name is an OXS object
    """
    return _unified_by_name(cls).is_instanceof("of_oxs")

def class_is_action(cls):
    """
    Return True if cls_name is an action object

    Note that action_id is not an action object, though it has
    the same header.  It looks like an action header, but the type
    is used to identify a kind of action, it does not indicate the
    type of the object following.
    """
    return _unified_by_name(cls).is_instanceof("of_action")

def class_is_action_id(cls):
    """
    Return True if cls_name is an action object

    Note that action_id is not an action object, though it has
    the same header.  It looks like an action header, but the type
    is used to identify a kind of action, it does not indicate the
    type of the object following.
    """
    return _unified_by_name(cls).is_instanceof("of_action_id")

def class_is_instruction(cls):
    """
    Return True if cls_name is an instruction object
    """
    return _unified_by_name(cls).is_instanceof("of_instruction")

def class_is_meter_band(cls):
    """
    Return True if cls_name is an instruction object
    """
    return _unified_by_name(cls).is_instanceof("of_meter_band")

def class_is_hello_elem(cls):
    """
    Return True if cls_name is an instruction object
    """
    return _unified_by_name(cls).is_instanceof("of_hello_elem")

def class_is_queue_prop(cls):
    """
    Return True if cls_name is a queue_prop object
    """
    return _unified_by_name(cls).is_instanceof("of_queue_prop")

def class_is_table_feature_prop(cls):
    """
    Return True if cls_name is a queue_prop object
    """
    return _unified_by_name(cls).is_instanceof("of_table_feature_prop")

def class_is_stats_message(cls):
    """
    Return True if cls_name is a message object based on info in unified
    """
    u = _unified_by_name(cls)
    return u.is_instanceof("of_stats_request") or u.ir_instanceof("of_stats_reply")

def class_is_bsn_tlv(cls):
    """
    Return True if cls_name is a bsn_tlv object
    """
    return _unified_by_name(cls).is_instanceof("of_bsn_tlv")

def class_is_list(cls):
    """
    Return True if cls_name is a list object
    """
    return (cls.find("of_list_") == 0)

def class_is(cls, cand_name):
    return _unified_by_name(cls).is_instanceof(cand_name)

def type_is_of_object(m_type):
    """
    Return True if m_type is an OF object type
    """
    # Remove _t from the type id and see if key for unified class
    return _unified_by_name(re.sub(r'_t$', '', m_type)) != none_item

@memoize
def lookup_ir_wiretype(oftype, version):
    """ if of is a reference to an enum in ir, resolve it to the wiretype
        declared in that enum. Else return oftype """
    enums = loxi_globals.ir[version].enums
    enum = find(lambda e: e.name == oftype, enums)
    if enum and 'wire_type' in enum.params:
        return enum.params['wire_type']
    else:
        return oftype

@memoize
def lookup_ir_enum(oftype, version):
    """ if oftype is a reference to an enum in ir,
        return the value-name mapping; otherwise return None """
    enums = loxi_globals.ir[version].enums
    return find(lambda e: e.name == oftype, enums)

def oftype_is_list(oftype):
    return (oftype.find("list(") == 0)

# Converts "list(of_flow_stats_entry_t)" to "of_flow_stats_entry"
def oftype_list_elem(oftype):
    assert oftype.find("list(") == 0
    return oftype[5:-3]
