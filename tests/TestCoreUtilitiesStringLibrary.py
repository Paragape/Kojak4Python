"""
Created on February 7, 2017

@author: John Jackson
"""

import unittest
from kojak.core.utilities.StringLibrary import StringLibrary
from kojak.core.Exceptions import HardException
import os
import re


class TestCoreUtilitiesStringLibrary(unittest.TestCase):

    #####################################################################################################
    # METHOD - addEscapeSequencesForDisplay
    #####################################################################################################

    def test_method_addEscapeSequencesForDisplay(self):
        self.assertEqual("a\\u0000b", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x00) + "b"))
        self.assertEqual("a\\bb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x08) + "b"))
        self.assertEqual("a\\tb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x09) + "b"))
        self.assertEqual("a\\nb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x0A) + "b"))
        self.assertEqual("a\\fb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x0C) + "b"))
        self.assertEqual("a\\rb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x0D) + "b"))
        self.assertEqual("a\\u001Fb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x1F) + "b"))
        self.assertEqual("a b", StringLibrary.addEscapeSequencesForDisplay("a b"))
        self.assertEqual("a\\\"b", StringLibrary.addEscapeSequencesForDisplay("a\"b"))
        self.assertEqual("a\\\\b", StringLibrary.addEscapeSequencesForDisplay("a\\b"))
        self.assertEqual("a/b", StringLibrary.addEscapeSequencesForDisplay("a/b"))
        self.assertEqual("a~b", StringLibrary.addEscapeSequencesForDisplay("a~b"))
        self.assertEqual("a\\u007Fb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x7F) + "b"))
        self.assertEqual("a\\u00FFb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0xFF) + "b"))
        self.assertEqual("a\\u0100b", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0x100) + "b"))
        self.assertEqual("a\\uFFFFb", StringLibrary.addEscapeSequencesForDisplay("a" + chr(0xFFFF) + "b"))

    ####################################################################################################
    # METHOD - addEscapeSequencesForRegex
    ####################################################################################################

    def test_method_addEscapeSequencesForRegex(self):
        self.assertEqual(r'foo\$\^\*\(\)\+\{\}\|\[\]\\\?\.bar', StringLibrary.addEscapeSequencesForRegex('foo$^*()+{}|[]\\?.bar'))

    ####################################################################################################
    # METHOD - addEscapeSequencesForStrings
    ####################################################################################################

    def test_method_addEscapeSequencesForStrings(self):
        self.assertEqual(r'1\"2\t3\n4\r5\\6', StringLibrary.addEscapeSequencesForStrings('1"2\t3\n4\r5\\6'))
        self.assertEqual(r'1\"2\t3\n4\r5\\6', StringLibrary.addEscapeSequencesForStrings('1"2\t3\n4\r5\\6', '&'))   # Invalid delimiter is ignored

        # Double-quoted strings
        self.assertEqual(r'1\"2\t3\n4\r5\\6', StringLibrary.addEscapeSequencesForStrings('1"2\t3\n4\r5\\6', '"'))

        # Single-quoted strings
        self.assertEqual(r"1\'2\t3\n4\r5\\6", StringLibrary.addEscapeSequencesForStrings("1'2\t3\n4\r5\\6", "'"))

    ####################################################################################################
    # METHOD - parseIntegerList
    ####################################################################################################

    def test_method_parseIntegerList(self):
        expected = [1, 2, 6, 7, 8, 9, 15, 14, 13, 12, -1, -3, -4, -5, -6, -7, -10, -9, -8]
        self.assertEquals(expected, StringLibrary.parseIntegerList(" 1,     2,6..9,   ,   15..12,-1,-3..-7,-10..-8"))

    def test_method_parseIntegerListEmpty(self):
        expected = []
        self.assertEquals(expected, StringLibrary.parseIntegerList("    "))

    def test_method_parseIntegerListException(self):
        self.assertRaisesRegex(HardException, "^HardException: Cannot parse 'foobar' from '1,foobar,5' into an integer list$", StringLibrary.parseIntegerList, "1,foobar,5")

    ####################################################################################################
    # METHOD - plural
    ####################################################################################################

    def test_method_plural(self):
        self.assertEquals('no pennies', StringLibrary.plural(0, 'no', 'penny', 'pennies'))
        self.assertEquals('1 penny', StringLibrary.plural(1, 'no', 'penny', 'pennies'))
        self.assertEquals('2 pennies', StringLibrary.plural(2, 'no', 'penny', 'pennies'))
        self.assertEquals('-1 pennies', StringLibrary.plural(-1, 'no', 'penny', 'pennies'))

    ####################################################################################################
    # METHOD - renderEscapeSequences
    ####################################################################################################

    def test_method_renderEscapeSequences(self):
        self.assertEquals(r'1"2\t3' + os.linesep + r'4\r5\6', StringLibrary.renderEscapeSequences(r'1\"2\t3' + os.linesep + r'4\r5\\6'))
        self.assertEquals(r"1'2\t3" + os.linesep + r'4\r5\6', StringLibrary.renderEscapeSequences(r"1\'2\t3" + os.linesep + r'4\r5\\6'))
        self.assertEquals('A', StringLibrary.renderEscapeSequences(r'\x41'))
        self.assertEquals('\u123F', StringLibrary.renderEscapeSequences(r'\u123F'))

    ####################################################################################################
    # METHOD - replaceAll
    ####################################################################################################

    def test_method_replaceAll(self):
        self.assertEquals(r'1 \-$Z\r\n 2 \-$Z\r\n 3', StringLibrary.replaceAll(re.compile(r'zzz'), '1 zzz 2 zzz 3', r'\-$Z\r\n'))

    ####################################################################################################
    # METHOD - stringify
    ####################################################################################################

    def test_method_stringify(self):
        self.assertEquals('null', StringLibrary.stringify(None))
        self.assertEquals('true', StringLibrary.stringify(True))
        self.assertEquals('false', StringLibrary.stringify(False))
        self.assertEquals('1', StringLibrary.stringify(1))
        self.assertEquals('2.3', StringLibrary.stringify(2.3))
        self.assertEquals('foo"bar', StringLibrary.stringify('foo"bar'))

    def test_method_stringify_withContext(self):
        self.assertEquals('null', StringLibrary.stringify(None, True))
        self.assertEquals('true', StringLibrary.stringify(True, True))
        self.assertEquals('false', StringLibrary.stringify(False, True))
        self.assertEquals('1', StringLibrary.stringify(1, True))
        self.assertEquals('2.3', StringLibrary.stringify(2.3, True))
        self.assertEquals('"foo\\"bar"', StringLibrary.stringify('foo"bar', True))

    ####################################################################################################
    # METHOD - toCsv
    ####################################################################################################

    def test_method_toCsv_None(self):
        source = None
        self.assertEquals('[]', StringLibrary.toCsv(source))

    def test_method_toCsv_Object(self):
        source = HardException('foobar')
        self.assertEquals('[HardException: foobar]', StringLibrary.toCsv(source))

    def test_method_toCsv_List(self):
        # Empty list
        source = []
        self.assertEquals('[]', StringLibrary.toCsv(source))

        # One element
        source = [1]
        self.assertEquals('[1]', StringLibrary.toCsv(source))

        # Multiple, mixed elements
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEquals('[null,true,false,1,2.3,foobar]', StringLibrary.toCsv(source))

        # Alternate Brackets and Separator
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEquals('<null:true:false:1:2.3:foobar>', StringLibrary.toCsv(source, '<', '>', ':'))

        # With context
        source = [None, True, False, 1, 2.3, "foobar"]
        self.assertEquals('[null,true,false,1,2.3,"foobar"]', StringLibrary.toCsv(source, show_context=True))

    def test_method_toCsv_Set(self):
        # Empty set
        source = set()
        self.assertEquals('[]', StringLibrary.toCsv(source))

        # One element
        source = {1}
        self.assertEquals('[1]', StringLibrary.toCsv(source))

        # Multiple, mixed elements
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEquals('[2,3.4,false,foobar,null,true]', StringLibrary.toCsv(source))

        # Alternate Brackets and Separator
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEquals('<2:3.4:false:foobar:null:true>', StringLibrary.toCsv(source, '<', '>', ':'))

        # With context
        source = {None, True, False, 2, 3.4, "foobar"}
        self.assertEquals('["foobar",2,3.4,false,null,true]', StringLibrary.toCsv(source, show_context=True))

    def test_method_toCsv_Dict(self):
        # Empty set
        source = {}
        self.assertEquals('[]', StringLibrary.toCsv(source))

        # One element
        source = {'key1': 1}
        self.assertEquals('[key1]', StringLibrary.toCsv(source))

        # Multiple, mixed elements
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEquals('[key2,key3p4,keyFalse,keyFoobar,keyNone,keyTrue]', StringLibrary.toCsv(source))

        # Alternate Brackets and Separator
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEquals('<key2:key3p4:keyFalse:keyFoobar:keyNone:keyTrue>', StringLibrary.toCsv(source, '<', '>', ':'))

        # With context
        source = {'keyNone': None, 'keyTrue': True, 'keyFalse': False, 'key2': 2, 'key3p4': 3.4, 'keyFoobar': "foobar"}
        self.assertEquals('["key2","key3p4","keyFalse","keyFoobar","keyNone","keyTrue"]', StringLibrary.toCsv(source, show_context=True))

    ####################################################################################################
    # METHOD - toDisplay
    ####################################################################################################

    def test_method_toDisplay_None(self):
        self.assertEquals('null', StringLibrary.toDisplay(None))

    def test_method_toDisplay_Boolean(self):
        self.assertEquals('true', StringLibrary.toDisplay(True))
        self.assertEquals('false', StringLibrary.toDisplay(False))

    def test_method_toDisplay_Integer(self):
        self.assertEquals('0', StringLibrary.toDisplay(0))
        self.assertEquals('1', StringLibrary.toDisplay(1))

    def test_method_toDisplay_Float(self):
        self.assertEquals('3.4', StringLibrary.toDisplay(3.4))

    def test_method_toDisplay_String(self):
        self.assertEquals('"foo\\"bar"', StringLibrary.toDisplay('foo"bar'))

    def test_method_toDisplay_StringWithPrefix(self):
        self.assertEquals('Prefix-"foo\\"bar"', StringLibrary.toDisplay('foo"bar', 'Prefix-'))

    def test_method_toDisplay_List(self):
        self.assertEquals('[]', StringLibrary.toDisplay([]))
        self.assertEquals('[null]', StringLibrary.toDisplay([None]))
        self.assertEquals('[true]', StringLibrary.toDisplay([True]))
        self.assertEquals('[5]', StringLibrary.toDisplay([5]))
        self.assertEquals('[123.456]', StringLibrary.toDisplay([123.456]))
        self.assertEquals('["foobar"]', StringLibrary.toDisplay(['foobar']))
        self.assertEquals('[["foobar"]]', StringLibrary.toDisplay([['foobar']]))
        self.assertEquals('[{}]', StringLibrary.toDisplay([{}]))

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
        self.assertEquals(expected, StringLibrary.toDisplay([None, True, 5, 123.456, 'foobar', ['foobar'], {'foo': 'bar'}]))

        expected: str = '' \
            + '[[[[' + os.linesep \
            + '    "foo",' + os.linesep \
            + '    "bar"' + os.linesep \
            + '    ]]]]'
        self.assertEquals(expected, StringLibrary.toDisplay([[[['foo', 'bar']]]]))

    def test_method_toDisplay_Dict(self):
        self.assertEquals('{}', StringLibrary.toDisplay({}))
        self.assertEquals('{null : null}', StringLibrary.toDisplay({None: None}))
        self.assertEquals('{true : false}', StringLibrary.toDisplay({True: False}))
        self.assertEquals('{5 : 7}', StringLibrary.toDisplay({5: 7}))
        self.assertEquals('{123.456 : 234.567}', StringLibrary.toDisplay({123.456: 234.567}))
        self.assertEquals('{"foobar" : "foo"}', StringLibrary.toDisplay({'foobar': 'foo'}))
        self.assertEquals('{"foobar" : {}}', StringLibrary.toDisplay({'foobar': {}}))

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
        self.assertEquals(expected, StringLibrary.toDisplay({None: None, True: False, 5: 7, 123.456: 234.567, 'foobar': 'foo', 'hello': ['foobar'], 'goodbye': {'foo': 'bar'}}))

        expected: str = '{1 : {2 : {3 : {4 : 5}}}}'
        self.assertEquals(expected, StringLibrary.toDisplay({1: {2: {3: {4: 5}}}}))

        expected: str = '' \
            + '{1 : {2 : {3 : {' + os.linesep \
            + '    4 : 5,' + os.linesep \
            + '    6 : [' + os.linesep \
            + '        7,' + os.linesep \
            + '        8' + os.linesep \
            + '        ]' + os.linesep \
            + '    }}}}'
        self.assertEquals(expected, StringLibrary.toDisplay({1: {2: {3: {4: 5, 6: [7, 8]}}}}))

    def test_method_toDisplay_RecursiveList(self):
        source: list = []
        source.append(source)
        self.assertRaisesRegex(HardException, "^HardException: Recursive list!$", StringLibrary.toDisplay, source)

    def test_method_toDisplay_RecursiveDict(self):
        source: dict = {}
        source['foobar'] = source
        self.assertRaisesRegex(HardException, "^HardException: Recursive dict!$", StringLibrary.toDisplay, source)

    #####################################################################################################
    # METHOD - toElapsedTime_D_HH_MM_SS_sss
    #####################################################################################################

    def test_method_toElapsedTime_D_HH_MM_SS_sss(self):
        self.assertEqual("14;06:56:07.890", StringLibrary.toElapsedTime_D_HH_MM_SS_sss(1234567890))
        self.assertEqual("-14;06:56:07.890", StringLibrary.toElapsedTime_D_HH_MM_SS_sss(-1234567890))

    #####################################################################################################
    # METHOD - toElapsedTimeVerbose
    #####################################################################################################
    
    def test_method_toElapsedTimeVerbose(self):
        self.assertEqual("0 seconds", StringLibrary.toElapsedTimeVerbose(0))
        self.assertEqual("1 millisecond", StringLibrary.toElapsedTimeVerbose(1))
        self.assertEqual("2 milliseconds", StringLibrary.toElapsedTimeVerbose(2))
        self.assertEqual("999 milliseconds", StringLibrary.toElapsedTimeVerbose(999))

        self.assertEqual("1 second", StringLibrary.toElapsedTimeVerbose(1000))
        self.assertEqual("1 second", StringLibrary.toElapsedTimeVerbose(1050))
        self.assertEqual("1.1 seconds", StringLibrary.toElapsedTimeVerbose(1051))
        self.assertEqual("1.5 seconds", StringLibrary.toElapsedTimeVerbose(1500))
        self.assertEqual("2.0 seconds", StringLibrary.toElapsedTimeVerbose(2000))
        self.assertEqual("90.0 seconds", StringLibrary.toElapsedTimeVerbose(90000))

        self.assertEqual("1.5 minutes", StringLibrary.toElapsedTimeVerbose(90001))
        self.assertEqual("90.0 minutes", StringLibrary.toElapsedTimeVerbose(5400000))
    
        self.assertEqual("1.5 hours", StringLibrary.toElapsedTimeVerbose(5400001))
        self.assertEqual("36.0 hours", StringLibrary.toElapsedTimeVerbose(129600000))
    
        self.assertEqual("1.5 days", StringLibrary.toElapsedTimeVerbose(129600001))
        self.assertEqual("10.5 days", StringLibrary.toElapsedTimeVerbose(907200000))
    
        self.assertEqual("1.5 weeks", StringLibrary.toElapsedTimeVerbose(907200001))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerbose(3628800000))
    
        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerbose(3628800001))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerbose(43545600000))
    
        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerbose(43545600001))
        self.assertEqual("3444.7 years", StringLibrary.toElapsedTimeVerbose(100000000000000))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseSeconds
    #####################################################################################################
    
    def test_method_toElapsedTimeVerboseSeconds(self):
        self.assertEqual("0 seconds", StringLibrary.toElapsedTimeVerboseSeconds(0.0))
        self.assertEqual("0.9 seconds", StringLibrary.toElapsedTimeVerboseSeconds(0.94))
        self.assertEqual("1 second", StringLibrary.toElapsedTimeVerboseSeconds(0.95))
        self.assertEqual("1 second", StringLibrary.toElapsedTimeVerboseSeconds(1.05))
        self.assertEqual("1.1 seconds", StringLibrary.toElapsedTimeVerboseSeconds(1.06))
        self.assertEqual("90.0 seconds", StringLibrary.toElapsedTimeVerboseSeconds(90.0))

        self.assertEqual("1.5 minutes", StringLibrary.toElapsedTimeVerboseSeconds(90.1))
        self.assertEqual("90.0 minutes", StringLibrary.toElapsedTimeVerboseSeconds(5400.0))

        self.assertEqual("1.5 hours", StringLibrary.toElapsedTimeVerboseSeconds(5400.1))
        self.assertEqual("36.0 hours", StringLibrary.toElapsedTimeVerboseSeconds(129600.0))
    
        self.assertEqual("1.5 days", StringLibrary.toElapsedTimeVerboseSeconds(129600.1))
        self.assertEqual("10.5 days", StringLibrary.toElapsedTimeVerboseSeconds(907200.0))
    
        self.assertEqual("1.5 weeks", StringLibrary.toElapsedTimeVerboseSeconds(907200.1))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerboseSeconds(3628800.0))
    
        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerboseSeconds(3628800.1))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerboseSeconds(43545600.0))
    
        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseSeconds(43545600.1))
        self.assertEqual("3444.7 years", StringLibrary.toElapsedTimeVerboseSeconds(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseMinutes
    #####################################################################################################
    
    def test_method_toElapsedTimeVerboseMinutes(self):
        self.assertEqual("0 minutes", StringLibrary.toElapsedTimeVerboseMinutes(0.0))
        self.assertEqual("0.9 minutes", StringLibrary.toElapsedTimeVerboseMinutes(0.94))
        self.assertEqual("1 minute", StringLibrary.toElapsedTimeVerboseMinutes(0.95))
        self.assertEqual("1 minute", StringLibrary.toElapsedTimeVerboseMinutes(1.05))
        self.assertEqual("1.1 minutes", StringLibrary.toElapsedTimeVerboseMinutes(1.06))
        self.assertEqual("90.0 minutes", StringLibrary.toElapsedTimeVerboseMinutes(90.0))

        self.assertEqual("1.5 hours", StringLibrary.toElapsedTimeVerboseMinutes(90.1))
        self.assertEqual("36.0 hours", StringLibrary.toElapsedTimeVerboseMinutes(2160.0))

        self.assertEqual("1.5 days", StringLibrary.toElapsedTimeVerboseMinutes(2160.1))
        self.assertEqual("10.5 days", StringLibrary.toElapsedTimeVerboseMinutes(15120.0))
    
        self.assertEqual("1.5 weeks", StringLibrary.toElapsedTimeVerboseMinutes(15120.1))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerboseMinutes(60480.0))
    
        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerboseMinutes(60480.1))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerboseMinutes(725760.0))
    
        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseMinutes(725760.1))
        self.assertEqual("206679.9 years", StringLibrary.toElapsedTimeVerboseMinutes(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseHours
    #####################################################################################################

    def test_method_toElapsedTimeVerboseHours(self):
        self.assertEqual("0 hours", StringLibrary.toElapsedTimeVerboseHours(0.0))
        self.assertEqual("0.9 hours", StringLibrary.toElapsedTimeVerboseHours(0.94))
        self.assertEqual("1 hour", StringLibrary.toElapsedTimeVerboseHours(0.95))
        self.assertEqual("1 hour", StringLibrary.toElapsedTimeVerboseHours(1.05))
        self.assertEqual("1.1 hours", StringLibrary.toElapsedTimeVerboseHours(1.06))
        self.assertEqual("36.0 hours", StringLibrary.toElapsedTimeVerboseHours(36.0))

        self.assertEqual("1.5 days", StringLibrary.toElapsedTimeVerboseHours(36.1))
        self.assertEqual("10.5 days", StringLibrary.toElapsedTimeVerboseHours(252.0))

        self.assertEqual("1.5 weeks", StringLibrary.toElapsedTimeVerboseHours(252.1))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerboseHours(1008.0))
    
        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerboseHours(1008.1))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerboseHours(12096.0))
    
        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseHours(12096.1))
        self.assertEqual("12400793.7 years", StringLibrary.toElapsedTimeVerboseHours(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseDays
    #####################################################################################################
    
    def test_method_toElapsedTimeVerboseDays(self):
        self.assertEqual("0 days", StringLibrary.toElapsedTimeVerboseDays(0.0))
        self.assertEqual("0.9 days", StringLibrary.toElapsedTimeVerboseDays(0.94))
        self.assertEqual("1 day", StringLibrary.toElapsedTimeVerboseDays(0.95))
        self.assertEqual("1 day", StringLibrary.toElapsedTimeVerboseDays(1.05))
        self.assertEqual("1.1 days", StringLibrary.toElapsedTimeVerboseDays(1.06))
        self.assertEqual("10.5 days", StringLibrary.toElapsedTimeVerboseDays(10.5))

        self.assertEqual("1.5 weeks", StringLibrary.toElapsedTimeVerboseDays(10.6))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerboseDays(42.0))

        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerboseDays(42.1))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerboseDays(504.0))
    
        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseDays(504.1))
        self.assertEqual("297619047.6 years", StringLibrary.toElapsedTimeVerboseDays(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseWeeks
    #####################################################################################################
    
    def test_method_toElapsedTimeVerboseWeeks(self):
        self.assertEqual("0 weeks", StringLibrary.toElapsedTimeVerboseWeeks(0.0))
        self.assertEqual("0.9 weeks", StringLibrary.toElapsedTimeVerboseWeeks(0.94))
        self.assertEqual("1 week", StringLibrary.toElapsedTimeVerboseWeeks(0.95))
        self.assertEqual("1 week", StringLibrary.toElapsedTimeVerboseWeeks(1.05))
        self.assertEqual("1.1 weeks", StringLibrary.toElapsedTimeVerboseWeeks(1.06))
        self.assertEqual("6.0 weeks", StringLibrary.toElapsedTimeVerboseWeeks(6.0))

        self.assertEqual("1.5 months", StringLibrary.toElapsedTimeVerboseWeeks(6.1))
        self.assertEqual("18.0 months", StringLibrary.toElapsedTimeVerboseWeeks(72.0))

        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseWeeks(72.1))
        self.assertEqual("2083333333.3 years", StringLibrary.toElapsedTimeVerboseWeeks(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseMonths
    #####################################################################################################

    def test_method_toElapsedTimeVerboseMonths(self):
        self.assertEqual("0 months", StringLibrary.toElapsedTimeVerboseMonths(0.0))
        self.assertEqual("0.9 months", StringLibrary.toElapsedTimeVerboseMonths(0.94))
        self.assertEqual("1 month", StringLibrary.toElapsedTimeVerboseMonths(0.95))
        self.assertEqual("1 month", StringLibrary.toElapsedTimeVerboseMonths(1.05))
        self.assertEqual("1.1 months", StringLibrary.toElapsedTimeVerboseMonths(1.06))

        self.assertEqual("1.5 years", StringLibrary.toElapsedTimeVerboseMonths(18.1))
        self.assertEqual("8333333333.3 years", StringLibrary.toElapsedTimeVerboseMonths(100000000000.0))

    #####################################################################################################
    # METHOD - toElapsedTimeVerboseYears
    #####################################################################################################

    def test_method_toElapsedTimeVerboseYears(self):
        self.assertEqual("0 years", StringLibrary.toElapsedTimeVerboseYears(0.0))
        self.assertEqual("0.9 years", StringLibrary.toElapsedTimeVerboseYears(0.94))
        self.assertEqual("1 year", StringLibrary.toElapsedTimeVerboseYears(0.95))
        self.assertEqual("1 year", StringLibrary.toElapsedTimeVerboseYears(1.05))
        self.assertEqual("1.1 years", StringLibrary.toElapsedTimeVerboseYears(1.06))
        self.assertEqual("100000000000.0 years", StringLibrary.toElapsedTimeVerboseYears(100000000000.0))

    ####################################################################################################
    # METHOD - toHexAscii
    ####################################################################################################

    def test_method_toHexAscii(self):
        self.assertEqual('466F6F6261720A', StringLibrary.toHexAscii('Foobar\n'))
        self.assertRaisesRegex(ValueError, "^The character 0x1234 is outside the ASCII range$", StringLibrary.toHexAscii, '\u1234')

    ####################################################################################################
    # METHOD - toRegexOrExpression
    ####################################################################################################

    def test_method_toRegexOrExpression_List(self):
        self.assertEqual('', StringLibrary.toRegexOrExpression([]))
        self.assertEqual('1', StringLibrary.toRegexOrExpression([1]))
        self.assertEqual('(?:null|true|false|1|2\\.3|hello)', StringLibrary.toRegexOrExpression([None, True, False, 1, 2.3, 'hello']))

    def test_method_toRegexOrExpression_Set(self):
        self.assertEqual('', StringLibrary.toRegexOrExpression(set()))
        self.assertEqual('1', StringLibrary.toRegexOrExpression({1}))
        # Note: In a set, True and 1 are the same.
        self.assertEqual(r'(?:2\.3|false|hello|null|true)', StringLibrary.toRegexOrExpression({None, True, False, 1, 2.3, 'hello'}))

