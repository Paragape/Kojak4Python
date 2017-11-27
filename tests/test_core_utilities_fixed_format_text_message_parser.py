"""
Created on November 24, 2017

@author: John Jackson
"""

import re
import unittest
from unittest import mock
from unittest.mock import call

from kojak.core.utilities import fixed_format_text_message_parser as mp
from test_utilities.test_utilities import verify_mock_calls

PATCH_LOGGER = 'kojak.core.utilities.fixed_format_text_message_parser.TestLogger'

PATCH_ADD_HEX_BYTES = 'kojak.core.utilities.fixed_format_text_message_parser.BitMap.add_hex_bytes'


###############################################################################
# TEST FixedFormatMessageParser
###############################################################################

class TestFixedFormatMessageParser(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_CONSTRUCTOR(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        # TEST DISABLE DEBUG
        x = mp.FixedFormatMessageParser('')
        self.assertEqual(x._message, '')
        self.assertFalse(x._enable_debug_mode)
        self.assertEqual(x._cursor, 0)
        self.assertEqual(x._cursor_last_parse, 0)
        self.assertIs(x._logger, mock_logger.return_value)
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST ENABLE DEBUG
        msg = 'message'
        x = mp.FixedFormatMessageParser(msg, True)
        self.assertEqual(x._message, msg)
        self.assertTrue(x._enable_debug_mode)
        self.assertEqual(x._cursor, 0)
        self.assertEqual(x._cursor_last_parse, 0)
        self.assertIs(x._logger, mock_logger.return_value)
        expected_calls = [
            call.l.info("About to parse '{}'", msg),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - __str__
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test___str__(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = 'message'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(str(x), msg)
        x._cursor = 4
        self.assertEqual(str(x), msg[4:])
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - assert_at_end_of_message
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_assert_at_end_of_message(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = 'message'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST NOT AT END OF MESSAGE
        emsg = "ParseException: Unexpected text at end of message: ''   starting_here=>'message'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.assert_at_end_of_message
        )
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST AT END OF MESSAGE
        x._cursor = len(msg)
        x.assert_at_end_of_message()
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - assert_blank
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_assert_blank(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '   message'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST NOT BLANK - N = None
        emsg = "ParseException: Expected blank field of length 10: ''   starting_here=>'   message'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.assert_blank
        )
        expected_calls = [
            call.l.info("Read '{}'", '   message'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST BLANK - N = 0
        x._cursor = 0
        x.assert_blank(0)
        self.assertEqual(x._cursor, 0)
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST BLANK - N = 3
        x._cursor = 0
        x.assert_blank(3)
        self.assertEqual(x._cursor, 3)
        expected_calls = [
            call.l.info("Read '{}'", '   '),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - assert_equal
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_assert_equal(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = 'message'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST EQUAL - value = None
        emsg = "ParseException: Attempt to compare using None: ''   starting_here=>'message'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.assert_equal, None
        )
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST NOT-EQUAL
        emsg = "ParseException: Expected value 'sam': ''   starting_here=>'message'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.assert_equal, 'sam'
        )
        expected_calls = [
            call.l.info("Read '{}'", 'mes'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST EQUAL
        x._cursor = 0
        x.assert_equal(msg)
        self.assertEqual(x._cursor, len(msg))
        expected_calls = [
            call.l.info("Read '{}'", 'message'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_characters
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_characters(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg1 = 'message1'
        msg2 = 'message2'
        msg = msg1 + msg2
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = ZERO
        result = x.get_characters(0)
        self.assertEqual(result, '')
        self.assertEqual(x._cursor, 0)
        expected_calls = [
            call.l.info("Read '{}'", ''),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N = NON-ZERO VALUE
        result = x.get_characters(len(msg1))
        self.assertEqual(result, msg1)
        self.assertEqual(x._cursor, len(msg1))
        expected_calls = [
            call.l.info("Read '{}'", msg1),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N = None
        result = x.get_characters()
        self.assertEqual(result, msg2)
        self.assertEqual(x._cursor, len(msg))
        expected_calls = [
            call.l.info("Read '{}'", msg2),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        emsg = "ParseException: Attempt to read past end-of-message (cursor=16 length=5): 'message1message2'   starting_here=>''"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.get_characters, 5
        )
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_characters_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_characters_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg1 = 'message1'
        sentinel1 = '<1>'
        msg2 = 'message2'
        sentinel2 = '<2>'
        msg = msg1 + sentinel1 + msg2 + sentinel2
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST HAPPY PATH
        result = x.get_characters_to_sentinel(sentinel1)
        self.assertEqual(result, msg1)
        self.assertEqual(x._cursor, len(msg1 + sentinel1))
        expected_calls = [
            call.l.info("Read '{}'", 'message1'),
            call.l.info("Read '{}'", '<1>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST SENTINEL = None
        emsg = "ParseException: Attempt to use None sentinel: 'message1<1>'   starting_here=>'message2<2>'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.get_characters_to_sentinel, None
        )
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST SENTINEL NOT FOUND
        emsg = "ParseException: Could not find sentinel '<x>': 'message1<1>'   starting_here=>'message2<2>'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.get_characters_to_sentinel, '<x>'
        )
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_cursor
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_cursor(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg1 = 'message1'
        x = mp.FixedFormatMessageParser(msg1, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(x.get_cursor(), 0)
        x._cursor = 123
        self.assertEqual(x.get_cursor(), 123)

        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_exception
    # =========================================================================

    def test_get_exception(self):
        pass
        # This is tested as a consequence of the other tests.

    # =========================================================================
    # METHOD - get_hex_ascii
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_hex_ascii(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('4142434445464748', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = VALUE
        result = x.get_hex_ascii(4)
        self.assertEqual(result, 'ABCD')
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '41424344'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N NOT SPECIFIED
        result = x.get_hex_ascii()
        self.assertEqual(result, 'EFGH')
        self.assertEqual(x._cursor, 16)
        expected_calls = [
            call.l.info("Read '{}'", '45464748'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_hex_ascii_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_hex_ascii_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('41424344<02>45464748', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        result = x.get_hex_ascii_to_sentinel('<02>')
        self.assertEqual(result, 'ABCD')
        self.assertEqual(x._cursor, 12)
        expected_calls = [
            call.l.info("Read '{}'", '41424344'),
            call.l.info("Read '{}'", '<02>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_ascii_decimal
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_ascii_decimal(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('12345678', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = VALUE
        result = x.get_integer_from_ascii_decimal(4)
        self.assertEqual(result, 1234)
        self.assertEqual(x._cursor, 4)
        expected_calls = [
            call.l.info("Read '{}'", '1234'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N NOT SPECIFIED
        result = x.get_integer_from_ascii_decimal()
        self.assertEqual(result, 5678)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '5678'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_ascii_decimal_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_ascii_decimal_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('1234<02>5678', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        result = x.get_integer_from_ascii_decimal_to_sentinel('<02>')
        self.assertEqual(result, 1234)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '1234'),
            call.l.info("Read '{}'", '<02>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_ascii_hex
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_ascii_hex(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('12ABCDEF', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = VALUE
        result = x.get_integer_from_ascii_hex(4)
        self.assertEqual(result, 0x12AB)
        self.assertEqual(x._cursor, 4)
        expected_calls = [
            call.l.info("Read '{}'", '12AB'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N NOT SPECIFIED
        result = x.get_integer_from_ascii_hex()
        self.assertEqual(result, 0xCDEF)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", 'CDEF'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_ascii_hex_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_ascii_hex_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('12AB<02>CDEF', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        result = x.get_integer_from_ascii_hex_to_sentinel('<02>')
        self.assertEqual(result, 0x12AB)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '12AB'),
            call.l.info("Read '{}'", '<02>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_hex_ascii_decimal
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_hex_ascii_decimal(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('3132333435363738', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = VALUE
        result = x.get_integer_from_hex_ascii_decimal(4)
        self.assertEqual(result, 1234)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '31323334'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N NOT SPECIFIED
        result = x.get_integer_from_hex_ascii_decimal()
        self.assertEqual(result, 5678)
        self.assertEqual(x._cursor, 16)
        expected_calls = [
            call.l.info("Read '{}'", '35363738'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_hex_ascii_decimal_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_hex_ascii_decimal_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('31323334<02>35363738', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        result = x.get_integer_from_hex_ascii_decimal_to_sentinel('<02>')
        self.assertEqual(result, 1234)
        self.assertEqual(x._cursor, 12)
        expected_calls = [
            call.l.info("Read '{}'", '31323334'),
            call.l.info("Read '{}'", '<02>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_hex_ascii_hex
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_hex_ascii_hex(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('3132414243444546', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST N = VALUE
        result = x.get_integer_from_hex_ascii_hex(4)
        self.assertEqual(result, 0x12AB)
        self.assertEqual(x._cursor, 8)
        expected_calls = [
            call.l.info("Read '{}'", '31324142'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST N NOT SPECIFIED
        result = x.get_integer_from_hex_ascii_hex()
        self.assertEqual(result, 0xCDEF)
        self.assertEqual(x._cursor, 16)
        expected_calls = [
            call.l.info("Read '{}'", '43444546'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_integer_from_hex_ascii_hex_to_sentinel
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_integer_from_hex_ascii_hex_to_sentinel(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        x = mp.FixedFormatMessageParser('31324142<02>43444546', True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        result = x.get_integer_from_hex_ascii_hex_to_sentinel('<02>')
        self.assertEqual(result, 0x12AB)
        self.assertEqual(x._cursor, 12)
        expected_calls = [
            call.l.info("Read '{}'", '31324142'),
            call.l.info("Read '{}'", '<02>'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_message
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_message(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertIs(x.get_message(), msg)
        self.assertIs(x.get_message(-1), msg)
        self.assertIs(x.get_message(0), msg)
        self.assertEqual(x.get_message(7), '789ABCDEF')
        self.assertEqual(x._cursor, 0)
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_last_parse
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_last_parse(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(x.get_last_parse(), '')

        x.assert_equal('0123')
        self.assertEqual(x.get_last_parse(), '0123')

        x.assert_equal('4567')
        x.assert_equal('89')
        x.assert_equal('A')
        self.assertEqual(x.get_last_parse(), '456789A')

        x.assert_equal('B')
        x.assert_equal('C')
        x.assert_equal('DEF')
        self.assertEqual(x.get_last_parse(), 'BCDEF')

        expected_calls = [
            call.l.info("Read '{}'", '0123'),
            call.l.info("Read '{}'", '4567'),
            call.l.info("Read '{}'", '89'),
            call.l.info("Read '{}'", 'A'),
            call.l.info("Read '{}'", 'B'),
            call.l.info("Read '{}'", 'C'),
            call.l.info("Read '{}'", 'DEF'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_remaining_message, get_remaining_message_length
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_get_remaining_message(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(x.get_remaining_message(), '0123456789ABCDEF')
        self.assertEqual(x.get_remaining_message_length(), 16)

        x.get_characters(4)
        self.assertEqual(x.get_remaining_message(), '456789ABCDEF')
        self.assertEqual(x.get_remaining_message_length(), 12)

        x.get_characters()
        self.assertEqual(x.get_remaining_message(), '')
        self.assertEqual(x.get_remaining_message_length(), 0)

        expected_calls = [
            call.l.info("Read '{}'", '0123'),
            call.l.info("Read '{}'", '456789ABCDEF'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - _parse_as_decimal_integer
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test__parse_as_decimal_integer(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(x._parse_as_decimal_integer(0, ''), 0)
        self.assertEqual(x._parse_as_decimal_integer(0, '42'), 42)

        emsg = "ParseException: Not a valid decimal value 'sam': ''   starting_here=>'0123456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x._parse_as_decimal_integer, 0, 'sam'
        )

    # =========================================================================
    # METHOD - _parse_as_hexadecimal_integer
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test__parse_as_hexadecimal_integer(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        self.assertEqual(x._parse_as_hexadecimal_integer(0, ''), 0)
        self.assertEqual(x._parse_as_hexadecimal_integer(0, '4C'), 0x4C)

        emsg = "ParseException: Not a valid hexadecimal value 'sam': ''   starting_here=>'0123456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x._parse_as_hexadecimal_integer, 0, 'sam'
        )

    # =========================================================================
    # METHOD - _parse_as_hex_ascii
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test__parse_as_hex_ascii(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST ODD LENGTH
        emsg = "ParseException: Even number of characters required for hex-ascii '414': ''   starting_here=>'0123456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x._parse_as_hex_ascii, 0, '414'
        )

        self.assertEqual(x._parse_as_hex_ascii(0, ''), '')
        self.assertEqual(x._parse_as_hex_ascii(0, '4142'), 'AB')

        emsg = "ParseException: Not a valid hex-ascii value '4X': '01'   starting_here=>'23456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x._parse_as_hex_ascii, 0, '414X43'
        )

    # =========================================================================
    # METHOD - peek_characters
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_peek_characters(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST CURSOR < 0
        emsg = "ParseException: Illegal cursor value: -1"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_characters, -1, 4
        )

        # TEST CURSOR > MESSAGE LENGTH
        emsg = "ParseException: Attempt to read past end-of-message (cursor=20 length=4): '0123456789ABCDEF'   starting_here=>''"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_characters, 20, 4
        )

        # TEST LENGTH < 0
        emsg = "ParseException: Illegal length: -1"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_characters, 0, -1
        )

        # TEST READ PAST END-OF-MESSAGE
        emsg = "ParseException: Attempt to read past end-of-message (cursor=8 length=9): '01234567'   starting_here=>'89ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_characters, 8, 9
        )

        # TEST HAPPY PATH
        self.assertEqual(x.peek_characters(4, 6), '456789')

        self.assertEqual(x._cursor, 0)

    # =========================================================================
    # METHOD - peek_equal
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_peek_equal(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST VALUE IS NONE
        emsg = "ParseException: Attempt to compare using a null value: ''   starting_here=>'0123456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_equal, None
        )

        # TEST HAPPY PATH
        self.assertTrue(x.peek_equal('0123'))
        self.assertFalse(x.peek_equal('4567'))

        self.assertEqual(x._cursor, 0)

    # =========================================================================
    # METHOD - test_equal
    # =========================================================================

    @mock.patch(PATCH_LOGGER)
    def test_test_equal(self, mock_logger):
        mm = mock.Mock()

        mock_logger.return_value = mock.Mock()
        mm.attach_mock(mock_logger.return_value, 'l')

        msg = '0123456789ABCDEF'
        x = mp.FixedFormatMessageParser(msg, True)
        # Clear mock calls from constructor
        mm.mock_calls.clear()

        # TEST VALUE IS NONE
        emsg = "ParseException: Attempt to compare using a null value: ''   starting_here=>'0123456789ABCDEF'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.peek_equal, None
        )

        # TEST HAPPY PATH
        self.assertTrue(x.test_equal('0123'))
        self.assertTrue(x.test_equal('4567'))
        self.assertFalse(x.test_equal('4567'))

        self.assertEqual(x._cursor, 12)


###############################################################################
# TEST BitMap
###############################################################################

class TestBitMap(unittest.TestCase):

    parser = mp.FixedFormatMessageParser('')

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    @mock.patch(PATCH_ADD_HEX_BYTES)
    def test_CONSTRUCTOR(self, mock_add_hex_bytes):
        mm = mock.Mock()
        mm.attach_mock(mock_add_hex_bytes, 'ahb')

        # TEST PARSER = NONE
        emsg = 'A FixedFormatMessageParser is required'
        self.assertRaisesRegex(
            AssertionError,
            '^' + re.escape(emsg) + '$',
            mp.BitMap, None
        )

        # TEST NO HEX_BYTES
        x = mp.BitMap(self.parser)
        self.assertIs(x._parser, self.parser)
        self.assertEqual(x._bits, {})
        self.assertEqual(x._next_bit, 1)
        self.assertEqual(x._scratchpad, {})
        expected_calls = [
            call.ahb(None),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

        # TEST WITH HEX_BYTES
        x = mp.BitMap(self.parser, '8C031')
        self.assertIs(x._parser, self.parser)
        self.assertEqual(x._bits, {})
        self.assertEqual(x._next_bit, 1)
        self.assertEqual(x._scratchpad, {})
        expected_calls = [
            call.ahb('8C031'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - add_hex_bytes
    # =========================================================================

    def test_add_hex_bytes(self):
        x = mp.BitMap(self.parser)

        # TEST WITH NONE
        x.add_hex_bytes(None)
        self.assertEqual(x._bits, {})
        self.assertEqual(x._next_bit, 1)

        # TEST WITH VALUE
        x.add_hex_bytes('8C031')
        self.assertEqual(x._bits, {
            1: True,
            2: False,
            3: False,
            4: False,
            5: True,
            6: True,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: True,
            16: True,
            17: False,
            18: False,
            19: False,
            20: True,
            })
        self.assertEqual(x._next_bit, 21)

    # =========================================================================
    # METHOD - bit_is_set
    # =========================================================================

    def test_bit_is_set(self):
        x = mp.BitMap(self.parser, '8C031')

        set_bits = {1, 5, 6, 15, 16, 20}

        for bit in range(100):
            if bit in set_bits:
                self.assertTrue(x.bit_is_set(bit), bit)
            else:
                self.assertFalse(x.bit_is_set(bit), bit)

    # =========================================================================
    # METHOD - contains_bit
    # =========================================================================

    def test_contains_bit(self):
        x = mp.BitMap(self.parser, '8C031')

        for bit in range(100):
            if 0 < bit <= 20:
                self.assertTrue(x.contains_bit(bit), bit)
            else:
                self.assertFalse(x.contains_bit(bit), bit)

    # =========================================================================
    # METHOD - get_scratchpad, put_scratchpad
    # =========================================================================

    def test_get_scratchpad(self):
        x = mp.BitMap(self.parser)

        self.assertIsNone(x.get_scratchpad('key'))

        self.assertIsNone(x.put_scratchpad('key', 1234))
        self.assertEqual(x.get_scratchpad('key'), 1234)

    # =========================================================================
    # METHOD - get_parser
    # =========================================================================

    def test_get_parser(self):
        x = mp.BitMap(self.parser)

        self.assertIs(x.get_parser(), self.parser)


###############################################################################
# TEST BitMapExec
###############################################################################

class TestBitMapExec(unittest.TestCase):

    class MyBitMapExec(mp.BitMapExec):
        def __init__(self):
            pass

        def execute(self, bitmap, row):
            super().execute(bitmap, row)

    # =========================================================================
    # METHOD - execute
    # =========================================================================

    def test_execute(self):
        x = self.MyBitMapExec()
        self.assertRaises(NotImplementedError, x.execute, None, None)


###############################################################################
# TEST BitMapExecutor
###############################################################################

class TestBitMapExecutor(unittest.TestCase):

    class MyBitMapExec(mp.BitMapExec):
        def __init__(self, bit, report_mock):
            self.bit = bit
            self.mock = report_mock

        def execute(self, bitmap, row):
            self.mock.execute(bitmap, row, self.bit)

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):
        x = mp.BitMapExecutor()
        self.assertEqual(x._exec_map, {})
        self.assertEqual(x._exec_order, [])

    # =========================================================================
    # METHOD - add_exec
    # =========================================================================

    def test_add_exec(self):

        def method1():
            pass

        lambda1 = lambda bitmap, row: method1()

        def method2():
            pass

        lambda2 = lambda bitmap, row: method2()

        def method3():
            pass

        lambda3 = lambda bitmap, row: method3()

        def method4():
            pass

        lambda4 = lambda bitmap, row: method4()

        x = mp.BitMapExecutor()

        # TEST HAPPY PATH
        x.add_exec(1, lambda1)
        x.add_exec(3, lambda3)
        x.add_exec(4, lambda4)
        x.add_exec(2, lambda2)
        expected = {
            1: lambda1,
            2: lambda2,
            3: lambda3,
            4: lambda4,
        }
        self.assertEqual(x._exec_map, expected)
        self.assertEqual(x._exec_order, [1, 3, 4, 2])

        # TEST BIT ALREADY DEFINED
        emsg = 'HardException: Bit 1 is already defined'
        self.assertRaisesRegex(
            mp.HardException,
            '^' + re.escape(emsg) + '$',
            x.add_exec, 1, lambda1
        )


    # =========================================================================
    # METHOD - execute
    # =========================================================================

    def test_execute(self):
        mm = mock.Mock()

        report_mock = mock.Mock()
        mm.attach_mock(report_mock, 'rm')

        parser = mp.FixedFormatMessageParser('3C5A3445556666aaaaaccccccdddddddffffffff')
        bitmap = mp.BitMap(parser, parser.get_characters(4))
        row_object = {}

        def unexpected(bm, row, bit):
            report_mock.parse(bm, row, bit)

        def parse(bm, row, bit, expected):
            bitmap.get_parser().assert_equal(expected)
            report_mock.parse(bm, row, bit, expected)

        x = mp.BitMapExecutor()
        x.add_exec(1, lambda bitmap, row: unexpected(bitmap, row, 1))
        x.add_exec(2, lambda bitmap, row: unexpected(bitmap, row, 2))
        x.add_exec(3, lambda bitmap, row: parse(bitmap, row, 3, '3'))
        x.add_exec(4, lambda bitmap, row: parse(bitmap, row, 4, '44'))
        x.add_exec(5, lambda bitmap, row: parse(bitmap, row, 5, '555'))
        x.add_exec(6, lambda bitmap, row: parse(bitmap, row, 6, '6666'))
        x.add_exec(7, lambda bitmap, row: unexpected(bitmap, row, 7))
        x.add_exec(8, lambda bitmap, row: unexpected(bitmap, row, 8))
        x.add_exec(9, lambda bitmap, row: unexpected(bitmap, row, 9))
        x.add_exec(10, lambda bitmap, row: parse(bitmap, row, 10, 'aaaaa'))
        x.add_exec(11, lambda bitmap, row: unexpected(bitmap, row, 11))
        x.add_exec(12, lambda bitmap, row: parse(bitmap, row, 12, 'cccccc'))
        x.add_exec(13, lambda bitmap, row: parse(bitmap, row, 13, 'ddddddd'))
        x.add_exec(14, lambda bitmap, row: unexpected(bitmap, row, 14))
        x.add_exec(15, lambda bitmap, row: parse(bitmap, row, 15, 'ffffffff'))
        x.add_exec(16, lambda bitmap, row: unexpected(bitmap, row, 16))
        x.execute(bitmap, row_object)
        parser.assert_at_end_of_message()
        expected_calls = [
            call.rm.parse(bitmap, row_object, 3, '3'),
            call.rm.parse(bitmap, row_object, 4, '44'),
            call.rm.parse(bitmap, row_object, 5, '555'),
            call.rm.parse(bitmap, row_object, 6, '6666'),
            call.rm.parse(bitmap, row_object, 10, 'aaaaa'),
            call.rm.parse(bitmap, row_object, 12, 'cccccc'),
            call.rm.parse(bitmap, row_object, 13, 'ddddddd'),
            call.rm.parse(bitmap, row_object, 15, 'ffffffff'),
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)

    def test_execute__undefined_bit(self):
        mm = mock.Mock()

        report_mock = mock.Mock()
        mm.attach_mock(report_mock, 'rm')

        parser = mp.FixedFormatMessageParser('3C5A3445556666aaaaaccccccdddddddffffffff')
        bitmap = mp.BitMap(parser, parser.get_characters(4))
        row_object = {}

        def parse(bm, row, bit, expected):
            bitmap.get_parser().assert_equal(expected)
            report_mock.parse(bm, row, bit, expected)

        x = mp.BitMapExecutor()
        x.add_exec(20, lambda bitmap, row: parse(bitmap, row, 20, ''))

        emsg = "ParseException: Attempt to process undefined bit 20: '3C5A'   starting_here=>'3445556666aaaaaccccccdddddddffffffff'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.execute, bitmap, row_object
        )

    def test_execute__null_executor(self):
        mm = mock.Mock()

        report_mock = mock.Mock()
        mm.attach_mock(report_mock, 'rm')

        parser = mp.FixedFormatMessageParser('3C5A3445556666aaaaaccccccdddddddffffffff')
        bitmap = mp.BitMap(parser, parser.get_characters(4))
        row_object = {}

        x = mp.BitMapExecutor()
        x.execute(bitmap, row_object)
        expected_calls = [
        ]
        verify_mock_calls(self, mm.mock_calls, expected_calls)
        self.assertEqual(parser.get_remaining_message(), '3445556666aaaaaccccccdddddddffffffff')

    def test_execute__user_exception(self):

        parser = mp.FixedFormatMessageParser('3C5A3445556666aaaaaccccccdddddddffffffff')
        bitmap = mp.BitMap(parser, parser.get_characters(4))
        row_object = {}

        def parse():
            raise ValueError('oh-oh')

        x = mp.BitMapExecutor()
        x.add_exec(3, lambda bitmap, row: parse())
        emsg = "ParseException: Received exception trying to parse bit 3: oh-oh: '3C5A'   starting_here=>'3445556666aaaaaccccccdddddddffffffff'"
        self.assertRaisesRegex(
            mp.ParseException,
            '^' + re.escape(emsg) + '$',
            x.execute, bitmap, row_object
        )
