"""
Created on February 7, 2017

@author: John Jackson
"""

import os
import re
import unittest
from typing import cast, Pattern

from kojak.core.exceptions import HardException
from kojak.core.utilities import string_library as sl


###############################################################################
# TEST MODULE
###############################################################################

class Test(unittest.TestCase):

    # =========================================================================
    # METHOD - add_escape_sequences_for_display
    # =========================================================================

    def test_add_escape_sequences_for_display(self):
        self.assertEqual("a\\u0000b", sl.add_escape_sequences_for_display("a" + chr(0x00) + "b"))
        self.assertEqual("a\\bb", sl.add_escape_sequences_for_display("a" + chr(0x08) + "b"))
        self.assertEqual("a\\tb", sl.add_escape_sequences_for_display("a" + chr(0x09) + "b"))
        self.assertEqual("a\\nb", sl.add_escape_sequences_for_display("a" + chr(0x0A) + "b"))
        self.assertEqual("a\\fb", sl.add_escape_sequences_for_display("a" + chr(0x0C) + "b"))
        self.assertEqual("a\\rb", sl.add_escape_sequences_for_display("a" + chr(0x0D) + "b"))
        self.assertEqual("a\\u001Fb", sl.add_escape_sequences_for_display("a" + chr(0x1F) + "b"))
        self.assertEqual("a b", sl.add_escape_sequences_for_display("a b"))
        self.assertEqual("a\\\"b", sl.add_escape_sequences_for_display("a\"b"))
        self.assertEqual("a\\\\b", sl.add_escape_sequences_for_display("a\\b"))
        self.assertEqual("a/b", sl.add_escape_sequences_for_display("a/b"))
        self.assertEqual("a~b", sl.add_escape_sequences_for_display("a~b"))
        self.assertEqual("a\\u007Fb", sl.add_escape_sequences_for_display("a" + chr(0x7F) + "b"))
        self.assertEqual("a\\u00FFb", sl.add_escape_sequences_for_display("a" + chr(0xFF) + "b"))
        self.assertEqual("a\\u0100b", sl.add_escape_sequences_for_display("a" + chr(0x100) + "b"))
        self.assertEqual("a\\uFFFFb", sl.add_escape_sequences_for_display("a" + chr(0xFFFF) + "b"))

    # =========================================================================
    # METHOD - add_escape_sequences_for_regex
    # =========================================================================

    def test_add_escape_sequences_for_regex(self):
        self.assertEqual(r'foo\$\^\*\(\)\+\{\}\|\[\]\\\?\.bar', sl.add_escape_sequences_for_regex('foo$^*()+{}|[]\\?.bar'))

    # =========================================================================
    # METHOD - add_escape_sequences_for_strings
    # =========================================================================

    def test_add_escape_sequences_for_strings(self):
        self.assertEqual(r'1\"2\t3\n4\r5\\6', sl.add_escape_sequences_for_strings('1"2\t3\n4\r5\\6'))
        self.assertEqual(r'1\"2\t3\n4\r5\\6', sl.add_escape_sequences_for_strings('1"2\t3\n4\r5\\6', '&'))   # Invalid delimiter is ignored

        # Double-quoted strings
        self.assertEqual(r'1\"2\t3\n4\r5\\6', sl.add_escape_sequences_for_strings('1"2\t3\n4\r5\\6', '"'))

        # Single-quoted strings
        self.assertEqual(r"1\'2\t3\n4\r5\\6", sl.add_escape_sequences_for_strings("1'2\t3\n4\r5\\6", "'"))

    # =========================================================================
    # METHOD - parse_integer_list
    # =========================================================================

    def test_parse_integer_list(self):
        expected = [1, 2, 6, 7, 8, 9, 15, 14, 13, 12, -1, -3, -4, -5, -6, -7, -10, -9, -8]
        self.assertEqual(expected, sl.parse_integer_list(" 1,     2,6..9,   ,   15..12,-1,-3..-7,-10..-8"))

    def test_parse_integer_list__empty(self):
        expected = []
        self.assertEqual(expected, sl.parse_integer_list("    "))

    def test_parse_integer_list__exception(self):
        self.assertRaisesRegex(HardException, "^HardException: Cannot parse 'foobar' from '1,foobar,5' into an integer list$", sl.parse_integer_list, "1,foobar,5")

    # =========================================================================
    # METHOD - plural
    # =========================================================================

    def test_plural(self):
        self.assertEqual('no pennies', sl.plural(0, 'no', 'penny', 'pennies'))
        self.assertEqual('1 penny', sl.plural(1, 'no', 'penny', 'pennies'))
        self.assertEqual('2 pennies', sl.plural(2, 'no', 'penny', 'pennies'))
        self.assertEqual('-1 pennies', sl.plural(-1, 'no', 'penny', 'pennies'))

    # =========================================================================
    # METHOD - render_escape_sequences
    # =========================================================================

    def test_render_escape_sequences(self):
        self.assertEqual(r'1"2\t3' + os.linesep + r'4\r5\6', sl.render_escape_sequences(r'1\"2\t3' + os.linesep + r'4\r5\\6'))
        self.assertEqual(r"1'2\t3" + os.linesep + r'4\r5\6', sl.render_escape_sequences(r"1\'2\t3" + os.linesep + r'4\r5\\6'))
        self.assertEqual('A', sl.render_escape_sequences(r'\x41'))
        self.assertEqual('\u123F', sl.render_escape_sequences(r'\u123F'))

    # =========================================================================
    # METHOD - replace_all
    # =========================================================================

    def test_replace_all(self):
        # Need to typecast re.compile to prevent a lint warning
        self.assertEqual(r'1 \-$Z\r\n 2 \-$Z\r\n 3', sl.replace_all(cast(Pattern, re.compile(r'zzz')), '1 zzz 2 zzz 3', r'\-$Z\r\n'))

    # =========================================================================
    # METHOD - stringify
    # =========================================================================

    def test_stringify(self):
        self.assertEqual('null', sl.stringify(None))
        self.assertEqual('true', sl.stringify(True))
        self.assertEqual('false', sl.stringify(False))
        self.assertEqual('1', sl.stringify(1))
        self.assertEqual('2.3', sl.stringify(2.3))
        self.assertEqual('foo"bar', sl.stringify('foo"bar'))

    def test_stringify__with_context(self):
        self.assertEqual('null', sl.stringify(None, True))
        self.assertEqual('true', sl.stringify(True, True))
        self.assertEqual('false', sl.stringify(False, True))
        self.assertEqual('1', sl.stringify(1, True))
        self.assertEqual('2.3', sl.stringify(2.3, True))
        self.assertEqual('"foo\\"bar"', sl.stringify('foo"bar', True))

    # =========================================================================
    # METHOD - to_csv
    # =========================================================================

    def test_to_csv__none(self):
        source = None
        self.assertEqual('[]', sl.to_csv(source))

    def test_to_csv__object(self):
        source = HardException('foobar')
        self.assertEqual('[HardException: foobar]', sl.to_csv(source))

    def test_to_csv__list(self):
        # Empty list
        source = []
        self.assertEqual('[]', sl.to_csv(source))

        # One element
        source = [1]
        self.assertEqual('[1]', sl.to_csv(source))

        # Multiple, mixed elements
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEqual('[null,true,false,1,2.3,foobar]', sl.to_csv(source))

        # Alternate Brackets and Separator
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEqual('<null:true:false:1:2.3:foobar>', sl.to_csv(source, '<', '>', ':'))

        # With context
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEqual('[null,true,false,1,2.3,"foobar"]', sl.to_csv(source, show_context=True))

    def test_to_csv__set(self):
        # Empty set
        source = set()
        self.assertEqual('[]', sl.to_csv(source))

        # One element
        source = {1}
        self.assertEqual('[1]', sl.to_csv(source))

        # Multiple, mixed elements
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEqual('[2,3.4,false,foobar,null,true]', sl.to_csv(source))

        # Alternate Brackets and Separator
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEqual('<2:3.4:false:foobar:null:true>', sl.to_csv(source, '<', '>', ':'))

        # With context
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEqual('["foobar",2,3.4,false,null,true]', sl.to_csv(source, show_context=True))

    def test_to_csv__dict(self):
        # Empty set
        source = {}
        self.assertEqual('[]', sl.to_csv(source))

        # One element
        source = {'key1': 1}
        self.assertEqual('[key1]', sl.to_csv(source))

        # Multiple, mixed elements
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEqual('[key2,key3p4,keyFalse,keyFoobar,keyNone,keyTrue]', sl.to_csv(source))

        # Alternate Brackets and Separator
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEqual('<key2:key3p4:keyFalse:keyFoobar:keyNone:keyTrue>', sl.to_csv(source, '<', '>', ':'))

        # With context
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEqual('["key2","key3p4","keyFalse","keyFoobar","keyNone","keyTrue"]', sl.to_csv(source, show_context=True))

    # =========================================================================
    # METHOD - to_display
    # =========================================================================

    def test_to_display__none(self):
        self.assertEqual('null', sl.to_display(None))

    def test_to_display__boolean(self):
        self.assertEqual('true', sl.to_display(True))
        self.assertEqual('false', sl.to_display(False))

    def test_to_display__integer(self):
        self.assertEqual('0', sl.to_display(0))
        self.assertEqual('1', sl.to_display(1))

    def test_to_display__float(self):
        self.assertEqual('3.4', sl.to_display(3.4))

    def test_to_display__string(self):
        self.assertEqual('"foo\\"bar"', sl.to_display('foo"bar'))

    def test_to_display__string_with_prefix(self):
        self.assertEqual('Prefix-"foo\\"bar"', sl.to_display('foo"bar', 'Prefix-'))

    def test_to_display__list(self):
        self.assertEqual('[]', sl.to_display([]))
        self.assertEqual('[null]', sl.to_display([None]))
        self.assertEqual('[true]', sl.to_display([True]))
        self.assertEqual('[5]', sl.to_display([5]))
        self.assertEqual('[123.456]', sl.to_display([123.456]))
        self.assertEqual('["foobar"]', sl.to_display(['foobar']))
        self.assertEqual('[["foobar"]]', sl.to_display([['foobar']]))
        self.assertEqual('[{}]', sl.to_display([{}]))

        expected: str = '' \
            + '[' + os.linesep \
            + '    null,' + os.linesep \
            + '    true,' + os.linesep \
            + '    5,' + os.linesep \
            + '    123.456,' + os.linesep \
            + '    "foobar",' + os.linesep \
            + '    ["foobar"],' + os.linesep \
            + '    {"foo" : "bar"}' + os.linesep \
            + '    ]'
        self.assertEqual(expected, sl.to_display([None, True, 5, 123.456, 'foobar', ['foobar'], {'foo': 'bar'}]))

        expected: str = '' \
            + '[[[[' + os.linesep \
            + '    "foo",' + os.linesep \
            + '    "bar"' + os.linesep \
            + '    ]]]]'
        self.assertEqual(expected, sl.to_display([[[['foo', 'bar']]]]))

    def test_to_display__dict(self):
        self.assertEqual('{}', sl.to_display({}))
        self.assertEqual('{null : null}', sl.to_display({None: None}))
        self.assertEqual('{true : false}', sl.to_display({True: False}))
        self.assertEqual('{5 : 7}', sl.to_display({5: 7}))
        self.assertEqual('{123.456 : 234.567}', sl.to_display({123.456: 234.567}))
        self.assertEqual('{"foobar" : "foo"}', sl.to_display({'foobar': 'foo'}))
        self.assertEqual('{"foobar" : {}}', sl.to_display({'foobar': {}}))

        expected: str = '' \
            + '{' + os.linesep \
            + '    "foobar" : "foo",' + os.linesep \
            + '    "goodbye" : {"foo" : "bar"},' + os.linesep \
            + '    "hello" : ["foobar"],' + os.linesep \
            + '    123.456 : 234.567,' + os.linesep \
            + '    5 : 7,' + os.linesep \
            + '    null : null,' + os.linesep \
            + '    true : false' + os.linesep \
            + '    }'
        self.assertEqual(expected, sl.to_display({None: None, True: False, 5: 7, 123.456: 234.567, 'foobar': 'foo', 'hello': ['foobar'], 'goodbye': {'foo': 'bar'}}))

        expected: str = '{1 : {2 : {3 : {4 : 5}}}}'
        self.assertEqual(expected, sl.to_display({1: {2: {3: {4: 5}}}}))

        expected: str = '' \
            + '{1 : {2 : {3 : {' + os.linesep \
            + '    4 : 5,' + os.linesep \
            + '    6 : [' + os.linesep \
            + '        7,' + os.linesep \
            + '        8' + os.linesep \
            + '        ]' + os.linesep \
            + '    }}}}'
        self.assertEqual(expected, sl.to_display({1: {2: {3: {4: 5, 6: [7, 8]}}}}))

    def test_to_display__recursive_list(self):
        source: list = []
        source.append(source)
        self.assertRaisesRegex(HardException, "^HardException: Recursive list!$", sl.to_display, source)

    def test_to_display__recursive_dict(self):
        source: dict = {}
        source['foobar'] = source
        self.assertRaisesRegex(HardException, "^HardException: Recursive dict!$", sl.to_display, source)

    # =========================================================================
    # METHOD - to_elapsed_time_d_hh_mm_ss_sss
    # =========================================================================

    def test_to_elapsed_time_d_hh_mm_ss_sss(self):
        self.assertEqual("14;06:56:07.890", sl.to_elapsed_time_d_hh_mm_ss_sss(1234567890))
        self.assertEqual("-14;06:56:07.890", sl.to_elapsed_time_d_hh_mm_ss_sss(-1234567890))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose
    # =========================================================================

    def test_to_elapsed_time_verbose(self):
        self.assertEqual("0 seconds", sl.to_elapsed_time_verbose(0))
        self.assertEqual("1 millisecond", sl.to_elapsed_time_verbose(1))
        self.assertEqual("2 milliseconds", sl.to_elapsed_time_verbose(2))
        self.assertEqual("999 milliseconds", sl.to_elapsed_time_verbose(999))

        self.assertEqual("1 second", sl.to_elapsed_time_verbose(1000))
        self.assertEqual("1 second", sl.to_elapsed_time_verbose(1050))
        self.assertEqual("1.1 seconds", sl.to_elapsed_time_verbose(1051))
        self.assertEqual("1.5 seconds", sl.to_elapsed_time_verbose(1500))
        self.assertEqual("2.0 seconds", sl.to_elapsed_time_verbose(2000))
        self.assertEqual("90.0 seconds", sl.to_elapsed_time_verbose(90000))

        self.assertEqual("1.5 minutes", sl.to_elapsed_time_verbose(90001))
        self.assertEqual("90.0 minutes", sl.to_elapsed_time_verbose(5400000))

        self.assertEqual("1.5 hours", sl.to_elapsed_time_verbose(5400001))
        self.assertEqual("36.0 hours", sl.to_elapsed_time_verbose(129600000))

        self.assertEqual("1.5 days", sl.to_elapsed_time_verbose(129600001))
        self.assertEqual("10.5 days", sl.to_elapsed_time_verbose(907200000))

        self.assertEqual("1.5 weeks", sl.to_elapsed_time_verbose(907200001))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose(3628800000))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose(3628800001))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose(43545600000))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose(43545600001))
        self.assertEqual("3444.7 years", sl.to_elapsed_time_verbose(100000000000000))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_seconds
    # =========================================================================

    def test_to_elapsed_time_verbose_seconds(self):
        self.assertEqual("0 seconds", sl.to_elapsed_time_verbose_seconds(0.0))
        self.assertEqual("0.9 seconds", sl.to_elapsed_time_verbose_seconds(0.94))
        self.assertEqual("1 second", sl.to_elapsed_time_verbose_seconds(0.95))
        self.assertEqual("1 second", sl.to_elapsed_time_verbose_seconds(1.05))
        self.assertEqual("1.1 seconds", sl.to_elapsed_time_verbose_seconds(1.06))
        self.assertEqual("90.0 seconds", sl.to_elapsed_time_verbose_seconds(90.0))

        self.assertEqual("1.5 minutes", sl.to_elapsed_time_verbose_seconds(90.1))
        self.assertEqual("90.0 minutes", sl.to_elapsed_time_verbose_seconds(5400.0))

        self.assertEqual("1.5 hours", sl.to_elapsed_time_verbose_seconds(5400.1))
        self.assertEqual("36.0 hours", sl.to_elapsed_time_verbose_seconds(129600.0))

        self.assertEqual("1.5 days", sl.to_elapsed_time_verbose_seconds(129600.1))
        self.assertEqual("10.5 days", sl.to_elapsed_time_verbose_seconds(907200.0))

        self.assertEqual("1.5 weeks", sl.to_elapsed_time_verbose_seconds(907200.1))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose_seconds(3628800.0))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose_seconds(3628800.1))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose_seconds(43545600.0))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_seconds(43545600.1))
        self.assertEqual("3444.7 years", sl.to_elapsed_time_verbose_seconds(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_minutes
    # =========================================================================

    def test_to_elapsed_time_verbose_minutes(self):
        self.assertEqual("0 minutes", sl.to_elapsed_time_verbose_minutes(0.0))
        self.assertEqual("0.9 minutes", sl.to_elapsed_time_verbose_minutes(0.94))
        self.assertEqual("1 minute", sl.to_elapsed_time_verbose_minutes(0.95))
        self.assertEqual("1 minute", sl.to_elapsed_time_verbose_minutes(1.05))
        self.assertEqual("1.1 minutes", sl.to_elapsed_time_verbose_minutes(1.06))
        self.assertEqual("90.0 minutes", sl.to_elapsed_time_verbose_minutes(90.0))

        self.assertEqual("1.5 hours", sl.to_elapsed_time_verbose_minutes(90.1))
        self.assertEqual("36.0 hours", sl.to_elapsed_time_verbose_minutes(2160.0))

        self.assertEqual("1.5 days", sl.to_elapsed_time_verbose_minutes(2160.1))
        self.assertEqual("10.5 days", sl.to_elapsed_time_verbose_minutes(15120.0))

        self.assertEqual("1.5 weeks", sl.to_elapsed_time_verbose_minutes(15120.1))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose_minutes(60480.0))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose_minutes(60480.1))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose_minutes(725760.0))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_minutes(725760.1))
        self.assertEqual("206679.9 years", sl.to_elapsed_time_verbose_minutes(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_hours
    # =========================================================================

    def test_to_elapsed_time_verbose_hours(self):
        self.assertEqual("0 hours", sl.to_elapsed_time_verbose_hours(0.0))
        self.assertEqual("0.9 hours", sl.to_elapsed_time_verbose_hours(0.94))
        self.assertEqual("1 hour", sl.to_elapsed_time_verbose_hours(0.95))
        self.assertEqual("1 hour", sl.to_elapsed_time_verbose_hours(1.05))
        self.assertEqual("1.1 hours", sl.to_elapsed_time_verbose_hours(1.06))
        self.assertEqual("36.0 hours", sl.to_elapsed_time_verbose_hours(36.0))

        self.assertEqual("1.5 days", sl.to_elapsed_time_verbose_hours(36.1))
        self.assertEqual("10.5 days", sl.to_elapsed_time_verbose_hours(252.0))

        self.assertEqual("1.5 weeks", sl.to_elapsed_time_verbose_hours(252.1))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose_hours(1008.0))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose_hours(1008.1))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose_hours(12096.0))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_hours(12096.1))
        self.assertEqual("12400793.7 years", sl.to_elapsed_time_verbose_hours(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_days
    # =========================================================================

    def test_to_elapsed_time_verbose_days(self):
        self.assertEqual("0 days", sl.to_elapsed_time_verbose_days(0.0))
        self.assertEqual("0.9 days", sl.to_elapsed_time_verbose_days(0.94))
        self.assertEqual("1 day", sl.to_elapsed_time_verbose_days(0.95))
        self.assertEqual("1 day", sl.to_elapsed_time_verbose_days(1.05))
        self.assertEqual("1.1 days", sl.to_elapsed_time_verbose_days(1.06))
        self.assertEqual("10.5 days", sl.to_elapsed_time_verbose_days(10.5))

        self.assertEqual("1.5 weeks", sl.to_elapsed_time_verbose_days(10.6))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose_days(42.0))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose_days(42.1))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose_days(504.0))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_days(504.1))
        self.assertEqual("297619047.6 years", sl.to_elapsed_time_verbose_days(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_weeks
    # =========================================================================

    def test_to_elapsed_time_verbose_weeks(self):
        self.assertEqual("0 weeks", sl.to_elapsed_time_verbose_weeks(0.0))
        self.assertEqual("0.9 weeks", sl.to_elapsed_time_verbose_weeks(0.94))
        self.assertEqual("1 week", sl.to_elapsed_time_verbose_weeks(0.95))
        self.assertEqual("1 week", sl.to_elapsed_time_verbose_weeks(1.05))
        self.assertEqual("1.1 weeks", sl.to_elapsed_time_verbose_weeks(1.06))
        self.assertEqual("6.0 weeks", sl.to_elapsed_time_verbose_weeks(6.0))

        self.assertEqual("1.5 months", sl.to_elapsed_time_verbose_weeks(6.1))
        self.assertEqual("18.0 months", sl.to_elapsed_time_verbose_weeks(72.0))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_weeks(72.1))
        self.assertEqual("2083333333.3 years", sl.to_elapsed_time_verbose_weeks(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_months
    # =========================================================================

    def test_to_elapsed_time_verbose_months(self):
        self.assertEqual("0 months", sl.to_elapsed_time_verbose_months(0.0))
        self.assertEqual("0.9 months", sl.to_elapsed_time_verbose_months(0.94))
        self.assertEqual("1 month", sl.to_elapsed_time_verbose_months(0.95))
        self.assertEqual("1 month", sl.to_elapsed_time_verbose_months(1.05))
        self.assertEqual("1.1 months", sl.to_elapsed_time_verbose_months(1.06))

        self.assertEqual("1.5 years", sl.to_elapsed_time_verbose_months(18.1))
        self.assertEqual("8333333333.3 years", sl.to_elapsed_time_verbose_months(100000000000.0))

    # =========================================================================
    # METHOD - to_elapsed_time_verbose_years
    # =========================================================================

    def test_to_elapsed_time_verbose_years(self):
        self.assertEqual("0 years", sl.to_elapsed_time_verbose_years(0.0))
        self.assertEqual("0.9 years", sl.to_elapsed_time_verbose_years(0.94))
        self.assertEqual("1 year", sl.to_elapsed_time_verbose_years(0.95))
        self.assertEqual("1 year", sl.to_elapsed_time_verbose_years(1.05))
        self.assertEqual("1.1 years", sl.to_elapsed_time_verbose_years(1.06))
        self.assertEqual("100000000000.0 years", sl.to_elapsed_time_verbose_years(100000000000.0))

    # =========================================================================
    # METHOD - to_hex_ascii
    # =========================================================================

    def test_to_hex_ascii(self):
        self.assertEqual('466F6F6261720A', sl.to_hex_ascii('Foobar\n'))
        self.assertRaisesRegex(ValueError, "^The character 0x1234 is outside the ASCII range$", sl.to_hex_ascii, '\u1234')

    # =========================================================================
    # METHOD - to_regex_or_expression
    # =========================================================================

    def test_to_regex_or_expression__list(self):
        self.assertEqual('', sl.to_regex_or_expression([]))
        self.assertEqual('1', sl.to_regex_or_expression([1]))
        self.assertEqual('(?:null|true|false|1|2\\.3|hello)', sl.to_regex_or_expression([None, True, False, 1, 2.3, 'hello']))

    def test_to_regex_or_expression__set(self):
        self.assertEqual('', sl.to_regex_or_expression(set()))
        self.assertEqual('1', sl.to_regex_or_expression({1}))
        # Note: In a set, True and 1 are the same.
        self.assertEqual(r'(?:2\.3|false|hello|null|true)', sl.to_regex_or_expression({None, True, False, 1, 2.3, 'hello'}))

