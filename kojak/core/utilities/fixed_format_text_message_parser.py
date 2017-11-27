"""
Created on November 18, 2017

@author: John Jackson
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, List, Optional

from kojak.core.exceptions import HardException
from kojak.core.test_logger import TestLogger


###############################################################################
# EXCEPTIONS
###############################################################################


class ParseException(HardException):
    """
    Raised to indicate that a parse exception has occurred.
    """
    pass


###############################################################################
# CONSTANTS
###############################################################################

# Translates hex-ascii values to ascii; for example, '41' => 'A'.
_HEX_ASCII_TO_ASCII = {'{:02X}'.format(_): chr(_) for _ in range(256)}

# Translates a hextet into the bits that are set using network ordering.
_HEXTET_TO_SET_BITS = {
    '0': tuple(),
    '1': (4,),
    '2': (3,),
    '3': (3, 4),
    '4': (2,),
    '5': (2, 4),
    '6': (2, 3),
    '7': (2, 3, 4),
    '8': (1,),
    '9': (1, 4),
    'A': (1, 3),
    'B': (1, 3, 4),
    'C': (1, 2),
    'D': (1, 2, 4),
    'E': (1, 2, 3),
    'F': (1, 2, 3, 4),
}

###############################################################################
# FixedFormatMessageParser
###############################################################################


class FixedFormatMessageParser:
    """
    This class provides utilities for parsing fixed-format messages,
    such as binary or text messages transferred between banking software.

    :param message: The message to parse.
    :param enable_debug_mode: If set to True, the parses will log each piece
        of the message as it is parsed.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self, message: str, enable_debug_mode: bool = False):

        # Holds the message being parsed.
        self._message: str = message or ''

        # Set true when the caller wants to enable debug mode,
        # which logs parse information.
        self._enable_debug_mode: bool = enable_debug_mode

        # Holds the index of where to begin the next sub-parse of the message.
        self._cursor: int = 0

        # The characters between this cursor and *_cursor* are the characters
        # returned by *get_last_parse()*.
        self._cursor_last_parse: int = 0

        # Create a logger.
        self._logger: TestLogger = TestLogger()

        if self._enable_debug_mode:
            self._logger.info("About to parse '{}'", self._message)

    # =========================================================================
    # __str__
    # =========================================================================

    def __str__(self):
        """
        Returns the remainder of the unparsed message but does not move the
        cursor.
        """

        return self.get_remaining_message()

    # =========================================================================
    # assert_at_end_of_message
    # =========================================================================

    def assert_at_end_of_message(self) -> None:
        """
        Tests that the cursor is at the end of the message; if not, the method
        raises an exception. The method does not move the cursor.
        :raises ParseException: The cursor is not at the end of the message.
        """

        if self.get_remaining_message_length() > 0:
            raise self.get_exception(
                'Unexpected text at end of message', self._cursor)

    # =========================================================================
    # assert_blank
    # =========================================================================

    def assert_blank(self, n: Optional[int] = None) -> None:
        """
        Tests that the next N characters of the message are whitespace
        and moves the cursor forward N characters.  If you do not specify N
        then the remainder of the message is checked.  If N is zero then the
        method succeeds.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: Any of the next N characters in the message
            are not white space characters or the message has fewer than N
            remaining characters.
        """

        if n is None:
            n = self.get_remaining_message_length()

        # Save the current cursor location in case we raise an exception.
        cursor: int = self._cursor

        if n > 0 and not self.get_characters(n).isspace():
            raise self.get_exception(
                'Expected blank field of length {}'.format(n), cursor)

    # =========================================================================
    # assert_equal
    # =========================================================================

    def assert_equal(self, value: str) -> None:
        """
        Tests that the next characters of the message equal the given value
        and moves the cursor forward the length of the given value.

        :param value: The value to compare.
        :raises ParseException: The next characters of the message do not
            equal the given value, the message has fewer remaining
            characters than the length of the given value, or the given value
            is None.
        """

        if value is None:
            raise self.get_exception(
                'Attempt to compare using None', self._cursor)

        # Save the current cursor location in case we raise an exception.
        cursor: int = self._cursor

        if value != self.get_characters(len(value)):
            raise self.get_exception(
                "Expected value '{}'".format(value), cursor)

    # =========================================================================
    # get_characters
    # =========================================================================

    def get_characters(self, n: Optional[int] = None) -> str:
        """
        Returns the next N characters in the message and moves the cursor
        forward N characters.  If you do not specify N then the remainder
        of the message is returned.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N remaining
            characters.
        """

        # If n is unspecified then get the remaining length of the message.
        if n is None:
            n = self.get_remaining_message_length()

        value = self.peek_characters(self._cursor, n)
        self._cursor += n
        return value

    # =========================================================================
    # get_characters_to_sentinel
    # =========================================================================

    def get_characters_to_sentinel(self, sentinel: str) -> str:
        """
        Looks for the given sentinel in the message, returns the characters
        up to but not including the sentinel, and moves the cursor forward
        just past the end of the sentinel.

        For example, if the message contains 'hello<GS>goodbye<GS>' and you
        specify the sentinel string '<GS>' then the method returns the string
        'hello' and moves the cursor forward to point to the 'g' of 'goodbye'.

        :param sentinel: The sentinel marking the end of the characters
            to return.
        :raises ParseException: The sentinel is not found or is None.
        """

        if sentinel is None:
            raise self.get_exception(
                'Attempt to use None sentinel', self._cursor)

        index: int = self._message.find(sentinel, self._cursor)
        if index < 0:
            raise self.get_exception(
                "Could not find sentinel '{}'".format(sentinel), self._cursor)

        value: str = self.get_characters(index - self._cursor)
        self.get_characters(len(sentinel))
        return value

    # =========================================================================
    # get_cursor
    # =========================================================================

    def get_cursor(self) -> int:
        """
        Returns the value of the cursor.
        """

        return self._cursor

    # =========================================================================
    # get_exception
    # =========================================================================

    def get_exception(
            self, message: str,
            cursor: Optional[int] = None) -> ParseException:
        """
        Returns a ParseException containing the given message and identifying
        the offending location within the message being parsed.

        :param message: The exception message.
        :param cursor: The cursor position within the parse message where the
            exception was discovered.  If set to None, the offending location
            within the message being parsed is not displayed.
        """

        if cursor is None:
            msg = message
        else:
            msg = "{}: '{}'   starting_here=>'{}'".format(
                message, self._message[:cursor], self._message[cursor:])
        return ParseException(msg)

    # =========================================================================
    # get_hex_ascii
    # =========================================================================

    def get_hex_ascii(self, n: Optional[int] = None) -> str:
        """
        Reads the next N*2 characters in the message, interprets them as
        hex-ASCII byte values, converts them to a string, returns the resulting
        value, and moves the cursor forward N*2 characters.

        For example, if the next 10 characters in the message buffer are
        *4142434445* then the method returns the string 'ABCDE'.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N*2 remaining
            characters.
        """

        n = n*2 if n is not None else None

        return self._parse_as_hex_ascii(
            self._cursor, self.get_characters(n))

    # =========================================================================
    # get_hex_ascii_to_sentinel
    # =========================================================================

    def get_hex_ascii_to_sentinel(self, sentinel: str) -> str:
        """
        Looks for the given sentinel in the message, reads the characters up to
        but not including the sentinel, interprets the characters as hex-ASCII
        byte values, returns the value, and moves the cursor forward just past
        the end of the sentinel.

        For example, if the message contains '4142434445<GS>field<GS>' and you
        specify the terminator string '<GS>' then the method returns the string
        'ABCDE' and moves the cursor forward to point to the 'f' of 'field'.

        :param sentinel: The sentinel marking the end of the characters
            to read.
        :raises ParseException: The sentinel is not found or is None.
        """

        return self._parse_as_hex_ascii(
            self._cursor, self.get_characters_to_sentinel(sentinel))

    # =========================================================================
    # get_integer_from_ascii_decimal
    # =========================================================================

    def get_integer_from_ascii_decimal(
            self, n: Optional[int] = None) -> int:
        """
        Reads the next N characters in the message, interprets them as a
        decimal value, returns the value, and moves the cursor forward N
        characters.

        For example, if the next 4 characters in the message buffer are
        *0234* and you specify *n=4* then the method returns the integer 234.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N remaining
            characters or the value cannot be parsed as a decimal value.
        """

        return self._parse_as_decimal_integer(
            self._cursor, self.get_characters(n))

    # =========================================================================
    # get_integer_from_ascii_decimal_to_sentinel
    # =========================================================================

    def get_integer_from_ascii_decimal_to_sentinel(
            self, sentinel: str) -> int:
        """
        Looks for the given sentinel in the message, reads the characters up to
        but not including the sentinel, interprets the characters as a decimal
        value, returns the value, and moves the cursor forward just past
        the end of the sentinel.

        For example, if the message contains '12345<GS>field<GS>' and you
        specify the terminator string '<GS>' then the method returns the
        integer 12345 and moves the cursor forward to point to the 'f' of
        'field'.

        :param sentinel: The sentinel marking the end of the characters
            to read.
        :raises ParseException: The sentinel is not found or is None or the
            value cannot be parsed as a decimal value.
        """

        return self._parse_as_decimal_integer(
            self._cursor, self.get_characters_to_sentinel(sentinel))

    # =========================================================================
    # get_integer_from_ascii_hex
    # =========================================================================

    def get_integer_from_ascii_hex(self, n: Optional[int] = None) -> int:
        """
        Reads the next N characters in the message, interprets them as a
        hexadecimal value, returns the value, and moves the cursor forward N
        characters.

        For example, if the next 4 characters in the message buffer are
        *007F* and you specify *n=4* then the method returns the integer 127.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N remaining
            characters or the value cannot be parsed as a hexadecimal value.
        """

        return self._parse_as_hexadecimal_integer(
            self._cursor, self.get_characters(n))

    # =========================================================================
    # get_integer_from_ascii_hex_to_sentinel
    # =========================================================================

    def get_integer_from_ascii_hex_to_sentinel(
            self, sentinel: str) -> int:
        """
        Looks for the given sentinel in the message, reads the characters up to
        but not including the sentinel, interprets the characters as a
        hexadecimal value, returns the value, and moves the cursor forward
        just past the end of the sentinel.

        For example, if the message contains '07F<GS>field<GS>' and you
        specify the terminator string '<GS>' then the method returns the
        integer 127 and moves the cursor forward to point to the 'f' of
        'field'.

        :param sentinel: The sentinel marking the end of the characters
            to read.
        :raises ParseException: The sentinel is not found or is None or the
            value cannot be parsed as a hexadecimal value.
        """

        return self._parse_as_hexadecimal_integer(
            self._cursor, self.get_characters_to_sentinel(sentinel))

    # =========================================================================
    # get_integer_from_hex_ascii_decimal
    # =========================================================================

    def get_integer_from_hex_ascii_decimal(
            self, n: Optional[int] = None) -> int:
        """
        Reads the next N*2 characters in the message, interprets them as
        hex-ASCII byte values, converts them to a string, interprets the
        resulting value as a decimal value, returns the decimal value, and
        moves the cursor forward N*2 characters.

        For example, if the next 10 characters in the message buffer are
        *3031323334* and you specify n=5 then the method returns the integer
        1234.

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N*2 remaining
            characters or the value cannot be parsed as a decimal value.
        """

        return self._parse_as_decimal_integer(
            self._cursor, self.get_hex_ascii(n))

    # =========================================================================
    # get_integer_from_hex_ascii_decimal_to_sentinel
    # =========================================================================

    def get_integer_from_hex_ascii_decimal_to_sentinel(
            self, sentinel: str) -> int:
        """
        Looks for the given sentinel in the message, reads the characters up to
        but not including the sentinel, interprets the characters as hex-ASCII
        byte values, converts them to a string, interprets the resulting string
        as a decimal value, and moves the cursor forward just past the end
        of the sentinel.

        For example, if the message contains '3031323334<GS>field<GS>' and you
        specify the terminator string '<GS>' then the method returns the
        integer 1234 and moves the cursor forward to point to the 'f' of
        'field'.

        :param sentinel: The sentinel marking the end of the characters
            to read.
        :raises ParseException: The sentinel is not found or is None or the
            value cannot be parsed as a decimal value.
        """

        return self._parse_as_decimal_integer(
            self._cursor, self.get_hex_ascii_to_sentinel(sentinel))

    # =========================================================================
    # get_integer_from_hex_ascii_hex
    # =========================================================================

    def get_integer_from_hex_ascii_hex(
            self, n: Optional[int] = None) -> int:
        """
        Reads the next N*2 characters in the message, interprets them as
        hex-ASCII byte values, converts them to a string, interprets the
        resulting value as a hexadecimal value, returns the hexadecimal value,
        and moves the cursor forward N*2 characters.

        For example, if the next 6 characters in the message buffer are
        *303746* and you specify n=3 then the method returns the integer 127
        (hex 07F).

        :param n: The number of characters to read, or the remainder
            of the message if *n* is not specified.
        :raises ParseException: The message has fewer than N*2 remaining
            characters or the value cannot be parsed as a hexadecimal value.
        """

        return self._parse_as_hexadecimal_integer(
            self._cursor, self.get_hex_ascii(n))

    # =========================================================================
    # get_integer_from_hex_ascii_hex_to_sentinel
    # =========================================================================

    def get_integer_from_hex_ascii_hex_to_sentinel(
            self, sentinel: str) -> int:
        """
        Looks for the given sentinel in the message, reads the characters up to
        but not including the sentinel, interprets the characters as hex-ASCII
        byte values, converts them to a string, interprets the resulting string
        as a hexadecimal value, returns the hexadecimal value, and moves the
        cursor just past the end of the sentinel.

        For example, if the message contains '303746<GS>field<GS>' and you
        specify the terminator string '<GS>' then the method returns the
        integer 127 (hex 07F) and moves the cursor forward to point to the
        'f' of 'field'.

        :param sentinel: The sentinel marking the end of the characters
            to read.
        :raises ParseException: The sentinel is not found or is None or the
            value cannot be parsed as a hexadecimal value.
        """

        return self._parse_as_hexadecimal_integer(
            self._cursor, self.get_hex_ascii_to_sentinel(sentinel))

    # =========================================================================
    # get_message
    # =========================================================================

    def get_message(self, cursor: Optional[int] = None) -> str:
        """
        Returns the message being parsed.

        :param cursor: The starting index, or the entire message if *cursor*
            is not specified.
        """

        if cursor is None or cursor <= 0:
            return self._message
        else:
            return self._message[cursor:]

    # =========================================================================
    # get_last_parse
    # =========================================================================

    def get_last_parse(self) -> str:
        """
        Returns a copy of what has been parsed up to this point since the
        last time this method was called.
        """

        msg = self._message[self._cursor_last_parse:self._cursor]
        self._cursor_last_parse = self._cursor
        return msg

    # =========================================================================
    # get_remaining_message
    # =========================================================================

    def get_remaining_message(self) -> str:
        """
        Returns the remainder of the unparsed message but does not move the
        cursor.
        """

        return self.get_message(self._cursor)

    # =========================================================================
    # get_remaining_message_length
    # =========================================================================

    def get_remaining_message_length(self) -> int:
        """
        Returns the number of unparsed characters remaining in the message.
        """

        length = len(self._message) - self._cursor
        return length if length > 0 else 0

    # =========================================================================
    # parse_as_decimal_integer
    # =========================================================================

    def _parse_as_decimal_integer(self, cursor: int, value: str) -> int:
        """
        Parses the given value as a decimal integer and returns an integer
        value.  Returns zero if the value is the empty string.

        :param cursor: The cursor location where the value was removed from the
            message; used only to report failures.
        :param value: The value to parse.
        :raises ParseException: The value cannot be parsed as a decimal
            integer.
        """

        if not value:
            return 0

        try:
            return int(value)
        except ValueError:
            raise self.get_exception(
                "Not a valid decimal value '{}'".format(value), cursor)

    # =========================================================================
    # parse_as_hexadecimal_integer
    # =========================================================================

    def _parse_as_hexadecimal_integer(self, cursor: int, value: str) -> int:
        """
        Parses the given value as a hexadecimal integer and returns an integer
        value.  Returns zero if the value is the empty string.

        :param cursor: The cursor location where the value was removed from the
            message; used only to report failures.
        :param value: The value to parse.
        :raises ParseException: The value cannot be parsed as a hexadecimal
            integer.
        """

        if not value:
            return 0

        try:
            return int(value, 16)
        except ValueError:
            raise self.get_exception(
                "Not a valid hexadecimal value '{}'".format(value), cursor)

    # =========================================================================
    # parse_as_hex_ascii
    # =========================================================================

    def _parse_as_hex_ascii(self, cursor: int, value: str) -> str:
        """
        Parses the given value as a hex-ASCII string (e.g., '4142434445' parses
        to 'ABCDE') and returns the new string.

        :param cursor: The cursor location where the value was removed from the
            message; used only to report failures.
        :param value: The value to parse.
        :raises ParseException: The value cannot be parsed as hex-ascii.
        """

        if len(value) % 2 == 1:
            raise self.get_exception(
                "Even number of characters required for hex-ascii '{}'"
                .format(value), cursor)

        return_value = ''
        for i in range(0, len(value), 2):
            hex_ascii = value[i:i+2]
            xlat = _HEX_ASCII_TO_ASCII.get(hex_ascii, None)
            if xlat:
                return_value += xlat
            else:
                raise self.get_exception(
                    "Not a valid hex-ascii value '{}'".format(hex_ascii),
                    cursor+i)

        return return_value

    # =========================================================================
    # peek_characters
    # =========================================================================

    def peek_characters(self, cursor: int, length: int) -> str:
        """
        Reads and returns the characters in the message starting at the given
        cursor and for the given length.

        :param cursor: The cursor location to begin the read.
        :param length: The number of characters to read.
        :raises ParseException: The message has fewer than N remaining
            characters.
        """

        if cursor < 0:
            raise self.get_exception("Illegal cursor value: {}".format(cursor))
        elif length < 0:
            raise self.get_exception("Illegal length: {}".format(length))
        elif cursor + length > len(self._message):
            raise self.get_exception(
                "Attempt to read past end-of-message (cursor={} length={})"
                .format(cursor, length), cursor)

        value = self._message[cursor:cursor+length]
        if self._enable_debug_mode:
            self._logger.info("Read '{}'", value)
        return value

    # =========================================================================
    # peek_equal
    # =========================================================================

    def peek_equal(self, value: str) -> bool:
        """
        Returns true if the characters at the current cursor location match
        the given value.  The method does not modify the current cursor
        location.

        :param value: The value to compare.
        :raises ParseException: The message has fewer remaining characters
            than the given value or the given value is None.
        """

        if value is None:
            raise self.get_exception(
                'Attempt to compare using a null value', self._cursor)

        return value == self.peek_characters(self._cursor, len(value))

    # =========================================================================
    # test_equal
    # =========================================================================

    def test_equal(self, value: str) -> bool:
        """
        Returns true if the next N characters in the message equal the given
        value and moves the cursor forward the length of the given value.

        :param value: The value to compare.
        :raises ParseException: The message has fewer remaining characters
            than the given value or the given value is None.
        """

        if value is None:
            raise self.get_exception(
                'Attempt to compare using a null value', self._cursor)

        return value == self.get_characters(len(value))


###############################################################################
# BitMap
###############################################################################


class BitMap:
    """
    This class interprets a stream of hex bytes as a bit map.

    :param parser: The parser to associate with this bitmap.
    :param hex_bytes: The initial hex bytes to add to the bitmap.  The bits
        are numbered in network order, that is, the first byte contains bits
        1-8 with bit 1 being the most-significant bit, the second byte contains
        bits 9-16, etc.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(
            self, parser: FixedFormatMessageParser,
            hex_bytes: Optional[str] = None):

        assert parser is not None, 'A FixedFormatMessageParser is required'

        # Holds a reference to the parent parser.
        self._parser: FixedFormatMessageParser = parser

        # Indicates which bits in the bit map are present and set.
        self._bits: Dict[int, bool] = {}

        # Indicates the next bit number that can be added to the bitmap.
        self._next_bit: int = 1

        # A dictionary, typically indexed by bit number,
        # that holds information for later use.
        self._scratchpad: dict = {}

        self.add_hex_bytes(hex_bytes)

    # =========================================================================
    # add_hex_bytes
    # =========================================================================

    def add_hex_bytes(self, hex_bytes: Optional[str]) -> None:
        """
        Adds the given stream of hex bytes to the bitmap.  The hex bytes are
        interpreted as a stream of bits with the left-most bit being bit 1.
        You may call this method more than once; each time the method resumes
        from the bit number where it last left off.

        For example, if you supply the hex byte stream '135C' then the method
        sets bit numbers 4, 7, 8, 10, 12, 13, and 14 in the bit map.  If you
        supply a second hex byte stream '8001' then the method sets bit numbers
        17 and 32 in the bit map.

        :param hex_bytes: The hex bytes to add to the bit map.
        """

        if hex_bytes:
            for hextet in hex_bytes:
                set_bits = _HEXTET_TO_SET_BITS[hextet]
                for bit_number in range(1, 4+1):
                    self._bits[self._next_bit] = bit_number in set_bits
                    self._next_bit += 1

    # =========================================================================
    # bit_is_set
    # =========================================================================

    def bit_is_set(self, bit_number: int) -> bool:
        """
        Returns true if the given bit number is set in the bitmap.

        :param bit_number: The 1-based bit number to test.
        """

        return self._bits.get(bit_number, False)

    # =========================================================================
    # contains_bit
    # =========================================================================

    def contains_bit(self, bit_number: int) -> bool:
        """
        Returns true if the given bit number is defined in the bitmap.

        :param bit_number: The 1-based bit number to test.
        """

        return bit_number in self._bits

    # =========================================================================
    # get_scratchpad
    # =========================================================================

    def get_scratchpad(self, key: Any) -> Any:
        """
        Returns the scratchpad value that was stored from a previous call
        to *put_scratchpad*, or None if the key does not exist.

        :param key: The key of the value to return.
        """

        return self._scratchpad.get(key, None)

    # =========================================================================
    # get_parser
    # =========================================================================

    def get_parser(self) -> FixedFormatMessageParser:
        """
        Returns the parser associated with this bitmap.
        """

        return self._parser

    # =========================================================================
    # put_scratchpad
    # =========================================================================

    def put_scratchpad(self, key: Any, value: Any) -> None:
        """
        Sets a scratchpad value that you may later retrieve with
        *get_scratchpad*.

        :param key: The key of the value to store.
        :param value: The value to store.
        """

        self._scratchpad[key] = value


###############################################################################
# BitMapExec
###############################################################################


class BitMapExec(ABC):
    """
    Defines an entry in a BitMapExecutor table that defines how to process
    a portion of a message when a particular bit in a bitmap is found set.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # execute
    # =========================================================================

    @abstractmethod
    def execute(self, bitmap: BitMap, row: Any) -> None:
        """
        Execute a custom parser operation on the given row data.

        :param bitmap: The bitmap containing this BitMapExec object.  From
            this bitmap user's can obtain the associated parser and scratchpad.
        :param row: The row data to parse.
        """

        raise NotImplementedError()


###############################################################################
# BitMapExecutor
###############################################################################


# TODO: TEST
class BitMapExecutor:
    """
    Defines a table that maps bit numbers to an executor that knows how
    to process a portion of a message if the associated bit is found set
    in a bitmap.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # __init__
    # =========================================================================

    def __init__(self):

        # Maps bit numbers to the executor that processes that bit number.
        self._exec_map: Dict[int, Callable[[BitMap, Any], None]] = {}

        # Tracks the order that entries in _exec_map were defined.
        # The BitMapExecuter will process the bits in that defined order
        # rather than in simple numerical order.
        self._exec_order: List[int] = []

    # =========================================================================
    # add_exec
    # =========================================================================

    def add_exec(
            self, bit_number: int, executor: Callable[[BitMap, Any], None]) -> None:
        """
        Associates an executor with a bit number.

        :param bit_number: The bit number.
        :param executor: The executor.
        :raises HardException: The bit number is already defined.
        """

        if bit_number in self._exec_map:
            raise HardException('Bit {} is already defined'.format(bit_number))

        self._exec_map[bit_number] = executor
        self._exec_order.append(bit_number)

    # =========================================================================
    # execute
    # =========================================================================

    def execute(self, bitmap: BitMap, row: Any) -> None:
        """
        Tests each bit in the bitmap in the order that the bits were added with
        *add_exec* if the bit is set in the bitmap then the method calls the
        associated executor.

        :param bitmap: The bitmap to query.
        :param row: An arbitrary object to receive the results of the actions
            of the executors.  This object will typically be a subclass of
            DtoCollection.DtoRow.
        :raises ParseException: A parse error has occurred.
        """

        parser: FixedFormatMessageParser = bitmap.get_parser()
        for bit_number in self._exec_order:
            # Get the cursor location for reporting errors.
            cursor: int = parser.get_cursor()
            # Raise exception if the bit is not defined.
            if not bitmap.contains_bit(bit_number):
                raise parser.get_exception(
                    'Attempt to process undefined bit {}'.format(bit_number),
                    cursor)
            # Call the bit executor if the bit is set.
            if bitmap.bit_is_set(bit_number):
                # Call the bit executor if one is defined.
                executor = self._exec_map.get(bit_number, None)
                if executor:
                    try:
                        executor(bitmap, row)
                    except Exception as e:
                        raise parser.get_exception(
                            'Received exception trying to parse bit {}: {}'
                            .format(bit_number, e), cursor)
