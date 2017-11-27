"""
Created on February 7, 2017

@author: John Jackson
"""

import os
import re
from typing import List, Pattern, Match

from kojak.core.exceptions import HardException

###########################################################################
# CONSTANTS - PUBLIC
###########################################################################

# Text symbols
SYMBOL_NULL: str = "null"
SYMBOL_FALSE: str = "false"
SYMBOL_TRUE: str = "true"

# Time conversion
MILLISECONDS_PER_SECOND: int = 1000
SECONDS_PER_MINUTE: int = 60
MINUTES_PER_HOUR: int = 60
HOURS_PER_DAY: int = 24
DAYS_PER_WEEK: int = 7
WEEKS_PER_MONTH: int = 4  # Only approximation required
MONTHS_PER_YEAR: int = 12

# Radix
RADIX_DECIMAL: int = 10
RADIX_HEXADECIMAL: int = 16

###########################################################################
# CONSTANTS - PRIVATE
###########################################################################

# Defines the threshold where the ``toStringElapsedTimeVerbose...`` methods
# switch from one unit to the next. For example, with a value of 1.5, the
# ``to_elapsed_time_verbose_seconds`` method hands control off to the
# ``to_elapsed_time_verbose_minutes`` method if the time value is greater
# than 90 (``SECONDS_PER_MINUTE`` * ``UNIT_THRESHOLD``).
_UNIT_THRESHOLD: float = 1.5

# Defines the +/- tolerance when comparing a float to an integer value
# such that we'll accept the float value is equal to the integer value.
_CLOSE_TO_VALUE: float = 0.05

# Specifies the number of spaces that the {@link #to_display} method uses
# to indent each level of a nested structure.
_TO_DISPLAY_INDENT: int = 4

# Specifies the smallest numerical value of the printable ASCII characters.
_MIN_PRINTABLE_ASCII_CHARACTER: int = 0x20

# Specifies the largest numerical value of the printable ASCII characters.
_MAX_PRINTABLE_ASCII_CHARACTER: int = 0x7E

# Specifies the largest numerical value of the ASCII character set.
_MAX_HEX_ASCII_VALUE: int = 0xFF

# Match:<non-printable-characters><double-quote><back-slash>
_MATCH_ESCAPABLE_CHARACTERS: Pattern = re.compile(
    r'[\x00-\x1F\x7F-\uFFFF"\\]')
# Maps special characters to transform by replacing the character with
# a back-slash followed by the mapped value of the character.
_TRANSLATE_ESCAPABLE_CHARACTERS: dict = {
    '"': r'\"',
    '\\': r'\\',
    '\b': r'\b',
    '\f': r'\f',
    '\n': r'\n',
    '\r': r'\r',
    '\t': r'\t',
}

_MATCH_ESCAPE_CHARACTERS_FOR_REGEX: Pattern = re.compile(
    r'[$^*()+{}|\[\]?.\\]')

# Match:<non-printable-characters><double-quote><back-slash>
_MATCH_ESCAPE_CHARACTERS_FOR_STRINGS: Pattern = re.compile(
    '["\'\n\r\t\\\\]')
# Maps special characters to transform by replacing the character with
# a back-slash followed by the mapped value of the character.
_TRANSLATE_ESCAPABLE_STRING_CHARACTERS: dict = {
    '\n': r'\n',
    '\r': r'\r',
    '\t': r'\t',
}

# Matches escape sequences for rendering them to their unescaped values.
_MATCH_ESCAPE_SEQUENCE: Pattern = re.compile(
    r'\\([^uxnrt]|u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2})')

# Matches integer values or ranges in a CSV list of integers.
_PARSE_INTEGER_LIST: Pattern = re.compile(r'([+-]?\d+)(?:\.\.([+-]?\d+))?')

###########################################################################
# METHODS
###########################################################################


# =========================================================================
# add_escape_sequences_for_display
# =========================================================================

def add_escape_sequences_for_display(value: str) -> str:
    """
    Replaces the non-ASCII and non-printable characters with escape
    sequences as well as the back-slash, forward-slash, and double-quote.

    :param value: The string to edit.
    :return: The edited string.
    """

    snippets: List[str] = []
    _add_escape_sequences_for_display_string(snippets, value)
    return ''.join(snippets)


def _add_escape_sequences_for_display_string(
        snippets: List[str], value: str, quote: str = "") -> None:
    """
    Copies the given string to the given snippets list while inserting
    escape sequences for all characters that match
    _MATCH_ESCAPABLE_CHARACTERS.  If **quote** is not None, the method
    inserts the value of **quote** on both ends of the string value.

    :param snippets: The list to receive the edits.
    :param value: The string to edit.
    :param quote: An optional character, such as a double-quote,
    to insert on each end of the edited value.
    """

    # Start with the quote character if one is provided.
    snippets.append(quote)

    # Replace the escapable sequences
    snippets.append(_MATCH_ESCAPABLE_CHARACTERS.sub(
        _add_escape_sequences_for_display_character, value))

    # End with the quote character if one is provided.
    snippets.append(quote)


def _add_escape_sequences_for_display_character(m: Match) -> str:
    """
    Returns the character in the given match object if the character
    is printable; returns the character as a printable escape sequence
    if the character is not printable.

    :param m: A match object matching a single character.
    :return: The translated character.
    """

    char = m.group(0)

    if char in _TRANSLATE_ESCAPABLE_CHARACTERS:
        return _TRANSLATE_ESCAPABLE_CHARACTERS.get(char)

    if _MIN_PRINTABLE_ASCII_CHARACTER <= ord(char)\
            <= _MAX_PRINTABLE_ASCII_CHARACTER:
        return char

    return r'\u{:04X}'.format(ord(char))


# =========================================================================
# add_escape_sequences_for_regex
# =========================================================================

def add_escape_sequences_for_regex(value: str) -> str:
    """
    Replaces the regex operator characters with escape sequences.

    :param value: The string to edit.
    """
    # Replace the regex operators.

    return _MATCH_ESCAPE_CHARACTERS_FOR_REGEX.sub(
        lambda m: '\\' + m.group(0), value)


# =========================================================================
# add_escape_sequences_for_strings
# =========================================================================

def add_escape_sequences_for_strings(value: str, delimiter: str = '"') -> str:
    """
    Replaces the back-slash, double-quote, single-quote, tab, new-line,
    and carriage-return characters with escape sequences.

    :param value: The string to edit.
    :param delimiter: This value will be backslash-escaped.  Only single-
    and double-quotes are allowed; all other values, including null,
    are defaulted to the double-quote.
    :return: The edited string.
    """

    # Verify the specified delimiter and select the delimiter that
    # we will _not_ escape.
    delimiter_to_leave_alone: str = '"' if delimiter == "'"\
        else "'" if delimiter == '"' else "'"

    return _MATCH_ESCAPE_CHARACTERS_FOR_STRINGS.sub(
        (lambda m: m.group(0) if m.group(0) == delimiter_to_leave_alone
            else _TRANSLATE_ESCAPABLE_STRING_CHARACTERS.get(m.group(0))
            if m.group(0) in _TRANSLATE_ESCAPABLE_STRING_CHARACTERS
            else '\\' + m.group(0)),
        value)


# =========================================================================
# parse_integer_list
# =========================================================================

def parse_integer_list(value: str) -> List[int]:
    """
    Parses a CSV list of integer values and/or integer ranges and returns
    an integer list containing the corresponding values.  For example,
    if <b>value</b> contains "1,2,6..9,15..12" then the return list
    contains the values "1,2,6,7,8,9,15,14,13,12".

    :param value: The string value to parse.
    :return: The corresponding list of integer values.
    """

    # Remove all white space.
    value = re.sub(r'\s', '', value)

    # If the value is empty then return an empty list
    if not value:
        return []

    values: List[int] = []

    for csvValue in value.split(','):

        # If this snippet is empty then ignore it.
        if len(csvValue) == 0:
            continue

        # Determine if the snippet is an integer value or integer range.
        m: Match = _PARSE_INTEGER_LIST.fullmatch(csvValue)
        # If neither then throw an exception.
        if not m:
            raise HardException(
                "Cannot parse '{}' from '{}' into an integer list"
                .format(csvValue, value))

        # If the snippet is an integer value then only group(1) will be
        # defined. If the snippet is an integer range, then both group(1)
        # and group(2) will be defined.
        value_from: int = int(m.group(1))
        value_to: int = int(m.group(m.lastindex))

        # Copy the value to the list.  If we are copying a range then copy
        # the values in the specified order, i.e., value_from to value_to
        # or value_from down to value_to.
        if value_from <= value_to:
            for i in range(value_from, value_to+1):
                values.append(i)
        else:
            for i in range(value_from, value_to-1, -1):
                values.append(i)

    return values


# =========================================================================
# plural
# =========================================================================

def plural(count: int, zero: str, single: str, multiple: str) -> str:
    """
    Returns the singular or plural text value depending on the specified
    numeric value.

    :param count: The number of items.
    :param zero: The value to write in place of zero if count==0.
    :param single: The value to return if count == 1.
    :param multiple: The value to return if count <> 1.
    """
    return '{} {}'.format(
        zero if count == 0 else str(count), single if count == 1 else multiple)


# =========================================================================
# render_escape_sequences
# =========================================================================

def render_escape_sequences(value: str) -> str:
    """
    Renders escape sequences in the string, for example, replaces "\x41"
    with 'A', but returns "\n", "\r", and "\t" unchanged.

    :param value: The string to edit.
    :return: The edited string.
    """

    # Replace the escapable sequences
    return _MATCH_ESCAPE_SEQUENCE.sub(
        _render_escape_sequences, value)


def _render_escape_sequences(m: Match) -> str:
    """
    Returns the character in the given match object if the character
    is printable; returns the character as a printable escape sequence
    if the character is not printable.

    :param m: A match object matching a single character.
    :return: The translated character.
    """

    token = m.group(1)[0:1]

    if token == 'u' or token == 'x':
        return chr(int(m.group(1)[1:], RADIX_HEXADECIMAL))

    return token


# =========================================================================
# replace_all
# =========================================================================

def replace_all(pattern: Pattern, source: str, replacement: str) -> str:
    """
    Similar to re.sub, but treats all characters in the replacement string
    as literal.

    :param pattern: The pattern to match.
    :param source: The string to edit.
    :param replacement: The value to replace each match.
    :return: The edited string.
    """

    # Use a lambda to avoid escape sequences.  Using the string itself
    # makes '\r', '\n', etc. susceptible for processing.
    return pattern.sub(lambda m: replacement, source)


# =========================================================================
# stringify
# =========================================================================

def stringify(value: object, show_context: bool = False) -> str:
    """
    Returns the normalized, stringified value of the given object.

    :param value: The value to stringify.
    :param show_context: Set to True to include double quotes around
    strings with embedded double quotes and backslashes escaped.
    :return: The stringified value.
    """

    if value is None:
        return SYMBOL_NULL

    if isinstance(value, bool):
        return SYMBOL_TRUE if value else SYMBOL_FALSE

    if show_context and isinstance(value, str):
        return '"' + add_escape_sequences_for_display(value) + '"'

    return str(value)


# =========================================================================
# to_csv
# =========================================================================

def to_csv(
        source: object, left_bracket: str = '[', right_bracket: str = ']',
        separator: str = ',', show_context: bool = False) -> str:
    """
    Returns a string containing the list representation of the stringified
        values of the source object.

    :param source: The object to process.

        * If the object is a list, the method returns the stringified
            values of the list items in list order.
        * If the object is a set, the method returns the stringified
            values of the set elements in alphabetical order.
        * If the object is a dict, the method returns the stringified
            values of the keys in alphabetical order.
        * If the object is anything else, the method returns the
            stringified value of the object.

    :param left_bracket: The character to use for the left bracket.
    :param right_bracket: The character to use for the right bracket.
    :param separator: The separator to place between the stringified
        values.
    :param show_context: Set to True to include double quotes around
        strings with embedded double quotes and backslashes escaped.
    :return: A csv list of the values in the source object.
    """

    snippets: list = []

    if source is not None:
        if isinstance(source, list):
            snippets = [stringify(element, show_context)
                        for element in source]
        elif isinstance(source, set):
            snippets = [stringify(element, show_context)
                        for element in source]
            snippets.sort()
        elif isinstance(source, dict):
            snippets = [stringify(key, show_context)
                        for key in source.keys()]
            snippets.sort()
        else:
            snippets = [stringify(source, show_context)]

    return left_bracket + separator.join(snippets) + right_bracket


# =========================================================================
# to_display
# =========================================================================

def to_display(source: object, prefix: str = '') -> str:
    """
    Returns a string containing a pretty-printed 'dump' of the specified
    data structure.

    :param source: The object to display.
    :param prefix: An optional prefix to prepend to the result.
    :return: The rendered display value.
    """

    # This set tracks what we are currently processing in order to detect
    # recursive structures.
    seen_this: set = set()

    # Collects the snippets that form the final string.
    snippets: list = [prefix]

    _to_display_object(snippets, 0, source, seen_this)
    return ''.join(snippets)


def _to_display_object(
        snippets: list, indent: int, source: object,
        seen_this: set) -> None:
    """
    Determines the type of the source object and passes control
    to the appropriate handler.

    :param snippets: A list to receive the bits and pieces representing
        the given source object.
    :param indent: The indent level to prefix to the display of the given
        source object.
    :param source: The object to display.
    :param seen_this: A set that contains the identities of objects
        we are currently displaying; used to detect recursive structures.
    """

    # If the value is None then just output the null symbol.
    if source is None:
        snippets.append(SYMBOL_NULL)
        return

    if isinstance(source, list):
        _to_display_list(
            snippets, indent + _TO_DISPLAY_INDENT, source, seen_this)
    elif isinstance(source, dict):
        _td_display_dict(
            snippets, indent + _TO_DISPLAY_INDENT, source, seen_this)
    elif isinstance(source, str):
        # We enclose strings in quotes.
        _add_escape_sequences_for_display_string(snippets, source, '"')
    else:
        snippets.append(stringify(source))


def _to_display_add_new_line(snippets: list, indent: int) -> None:
    """
    Appends a newline to the given snippets list as well as blanks making
    up the given indentation level.

    :param snippets: A list to receive the bits and pieces representing
        the given source object.
    :param indent: The indent level to prefix to the display of the given
        source object.
    """

    snippets.append(os.linesep)
    snippets.append(' ' * indent)


def _to_display_list(
        snippets: list, indent: int, source: list,
        seen_this: set) -> None:
    """
    Appends the values of the given source list to the snippets list.

    :param snippets: A list to receive the bits and pieces representing
        the given source list.
    :param indent: The indent level to prefix to the display of the given
        source list.
    :param source: The object to display.
    :param seen_this: A set that contains the identities of objects
        we are currently displaying; used to detect recursive structures.
    """

    # If we are already processing this list then throw an exception.
    if id(source) in seen_this:
        raise HardException('Recursive list!')
    # Record that we are processing the list.
    seen_this.add(id(source))

    snippets.append('[')

    if len(source) == 0:
        pass
    elif len(source) == 1:
        # If the list has only one entry then put the result on the same
        # line as the brackets.
        _to_display_object(
            snippets, indent - _TO_DISPLAY_INDENT, source[0],
            seen_this)
    else:
        # Construct the display value of the list and add it to the
        # snippets list.
        local_snippets: list = []
        for element in source:
            if len(local_snippets) > 0:
                local_snippets.append(',')
            _to_display_add_new_line(local_snippets, indent)
            _to_display_object(
                local_snippets, indent, element, seen_this)
        _to_display_add_new_line(local_snippets, indent)
        snippets.append(''.join(local_snippets))

    snippets.append(']')

    # Record that we are no longer processing this list.
    seen_this.discard(id(source))


def _td_display_dict(
        snippets: list, indent: int, source: dict,
        seen_this: set) -> None:
    """
    Appends the values of the given source dictionary to the snippets list.

    :param snippets: A list to receive the bits and pieces representing
        the given source dict.
    :param indent: The indent level to prefix to the display of the given
        source dict.
    :param source: The object to display.
    :param seen_this: A set that contains the identities of objects we are
        currently displaying; used to detect recursive structures.
    """

    # If we are already processing this dict then throw an exception.
    if id(source) in seen_this:
        raise HardException('Recursive dict!')
    # Record that we are processing the dict.
    seen_this.add(id(source))

    snippets.append('{')

    if len(source) == 0:
        pass
    elif len(source) == 1:
        # If the dictionary has only one entry then put the result on the
        # same line as the braces.
        _to_display_dict_single_entry(
            snippets, indent, source, seen_this)
    else:
        _to_display_dict_multi_entry(
            snippets, indent, source, seen_this)

    snippets.append('}')

    # Record that we are no longer processing this dict.
    seen_this.discard(id(source))


def _to_display_dict_single_entry(
        snippets: list, indent: int, source: dict,
        seen_this: set) -> None:
    """
    Appends the 'key : ' portion of this single-entry dictionary to the
    current display line. If the value is not a list or a dict then appends
    the value to the current display line as well.

    :param snippets: A list to receive the display value of the given
        source dict.
    :param indent: The indent level to prefix to the display of the given
        source dict.
    :param source: The object to display.
    :param seen_this: A set that contains the identities of objects we are
        currently displaying; used to detect recursive structures.
    """

    for k, v in source.items():
        _to_display_object(
            snippets, indent - _TO_DISPLAY_INDENT, k, seen_this)
        snippets.append(' : ')
        if isinstance(v, list):
            _to_display_list(snippets, indent, v, seen_this)
        elif isinstance(v, dict):
            _td_display_dict(snippets, indent, v, seen_this)
        else:
            _to_display_object(
                snippets, indent - _TO_DISPLAY_INDENT, v, seen_this)


def _to_display_dict_multi_entry(
        snippets: list, indent: int, source: dict,
        seen_this: set) -> None:
    """
    Sorts the given source dictionary by the stringified values of the keys
    then appends the key-value pairs to the snippets list, one key-value
    pair per line.

    :param snippets: A list to receive the display value of the given
        source dict.
    :param indent: The indent level to prefix to the display of the given
        source dict.
    :param source: The object to display.
    :param seen_this: A set that contains the identities of objects we are
        currently displaying; used to detect recursive structures.
    """

    # We want to be able to sort the keys alphabetically, but the keys are
    # not required to be strings; therefore, make a new dict where each key
    # is a string.
    temp_dict: dict = {}
    for key, value in source.items():
        temp_dict[stringify(key, True)] = value

    local_snippets: list = []
    for key in sorted(temp_dict):
        if len(local_snippets) > 0:
            local_snippets.append(',')
        _to_display_add_new_line(local_snippets, indent)
        local_snippets.append(key)
        local_snippets.append(' : ')
        _to_display_object(
            local_snippets, indent, temp_dict[key], seen_this)
    _to_display_add_new_line(local_snippets, indent)
    snippets.append(''.join(local_snippets))


# =========================================================================
# to_elapsed_time_d_hh_mm_ss_sss
# =========================================================================

def to_elapsed_time_d_hh_mm_ss_sss(milliseconds: int) -> str:
    """
    Returns a string describing the specified number of milliseconds
    in the format: D;HH:MM:SS.sss.

    :param milliseconds: The time period in milliseconds.
    """

    negative: bool = milliseconds < 0
    temp_time: int = -milliseconds if negative else milliseconds
    millis: int = temp_time % MILLISECONDS_PER_SECOND
    temp_time //= MILLISECONDS_PER_SECOND
    seconds: int = temp_time % SECONDS_PER_MINUTE
    temp_time //= SECONDS_PER_MINUTE
    minutes: int = temp_time % MINUTES_PER_HOUR
    temp_time //= MINUTES_PER_HOUR
    hours: int = temp_time % HOURS_PER_DAY
    temp_time //= HOURS_PER_DAY
    days: int = temp_time

    return '{:s}{:d};{:02d}:{:02d}:{:02d}.{:03d}'.format(
        '-' if negative else '', days, hours, minutes, seconds, millis)


# =========================================================================
# to_elapsed_time_verbose
# =========================================================================

def to_elapsed_time_verbose(milliseconds: int) -> str:
    """
    Returns a string describing the specified number of milliseconds in
    conversational tone, which means that it can describe time in terms
    of milliseconds, seconds, minutes, hours, days, weeks, months,
    or years.

    :param milliseconds: The time period in milliseconds.
    """

    if milliseconds == 0:
        return "0 seconds"

    if milliseconds == 1:
        return "1 millisecond"

    if milliseconds < MILLISECONDS_PER_SECOND:
        return '{:d} milliseconds'.format(milliseconds)

    return to_elapsed_time_verbose_seconds(
        milliseconds / MILLISECONDS_PER_SECOND)


# =========================================================================
# to_elapsed_time_verbose_seconds
# =========================================================================

def to_elapsed_time_verbose_seconds(seconds: float) -> str:
    """
    Returns a string describing the specified number of seconds in
    conversational tone, which means that it can describe time in terms
    of seconds, minutes, hours, days, weeks, months, or years.

    :param seconds: The time period in seconds.
    """

    if seconds < 0.0 + _CLOSE_TO_VALUE:
        return "0 seconds"

    if 1.0 - _CLOSE_TO_VALUE <= seconds <= 1.0 + _CLOSE_TO_VALUE:
        return "1 second"

    if seconds <= SECONDS_PER_MINUTE * _UNIT_THRESHOLD:
        return '{:3.1f} seconds'.format(seconds)

    return to_elapsed_time_verbose_minutes(
        seconds / SECONDS_PER_MINUTE)


# =========================================================================
# to_elapsed_time_verbose_minutes
# =========================================================================

def to_elapsed_time_verbose_minutes(minutes: float) -> str:
    """
    Returns a string describing the specified number of minutes in
    conversational tone, which means that it can describe time in terms
    of minutes, hours, days, weeks, months, or years.

    :param minutes: The time period in minutes.
    """

    if minutes < 0.0 + _CLOSE_TO_VALUE:
        return "0 minutes"

    if 1.0 - _CLOSE_TO_VALUE <= minutes <= 1.0 + _CLOSE_TO_VALUE:
        return "1 minute"

    if minutes <= MINUTES_PER_HOUR * _UNIT_THRESHOLD:
        return '{:3.1f} minutes'.format(minutes)

    return to_elapsed_time_verbose_hours(minutes / MINUTES_PER_HOUR)


# =========================================================================
# to_elapsed_time_verbose_hours
# =========================================================================

def to_elapsed_time_verbose_hours(hours: float) -> str:
    """
    Returns a string describing the specified number of hours in
    conversational tone, which means that it can describe time in terms
    of hours, days, weeks, months, or years.

    :param hours: The time period in hours.
    """

    if hours < 0.0 + _CLOSE_TO_VALUE:
        return "0 hours"

    if 1.0 - _CLOSE_TO_VALUE <= hours <= 1.0 + _CLOSE_TO_VALUE:
        return "1 hour"

    if hours <= HOURS_PER_DAY * _UNIT_THRESHOLD:
        return '{:3.1f} hours'.format(hours)

    return to_elapsed_time_verbose_days(hours / HOURS_PER_DAY)


# =========================================================================
# to_elapsed_time_verbose_days
# =========================================================================

def to_elapsed_time_verbose_days(days: float) -> str:
    """
    Returns a string describing the specified number of days in
    conversational tone, which means that it can describe time in terms
    of days, weeks, months, or years.

    :param days: The time period in days.
    """

    if days < 0.0 + _CLOSE_TO_VALUE:
        return "0 days"

    if 1.0 - _CLOSE_TO_VALUE <= days <= 1.0 + _CLOSE_TO_VALUE:
        return "1 day"

    if days <= DAYS_PER_WEEK * _UNIT_THRESHOLD:
        return '{:3.1f} days'.format(days)

    return to_elapsed_time_verbose_weeks(days / DAYS_PER_WEEK)


# =========================================================================
# to_elapsed_time_verbose_weeks
# =========================================================================

def to_elapsed_time_verbose_weeks(weeks: float) -> str:
    """
    Returns a string describing the specified number of weeks in
    conversational tone, which means that it can describe time in terms
    of weeks, months, or years.

    :param weeks: The time period in weeks.
    """

    if weeks < 0.0 + _CLOSE_TO_VALUE:
        return "0 weeks"

    if 1.0 - _CLOSE_TO_VALUE <= weeks <= 1.0 + _CLOSE_TO_VALUE:
        return "1 week"

    if weeks <= WEEKS_PER_MONTH * _UNIT_THRESHOLD:
        return '{:3.1f} weeks'.format(weeks)

    return to_elapsed_time_verbose_months(weeks / WEEKS_PER_MONTH)


# =========================================================================
# to_elapsed_time_verbose_months
# =========================================================================

def to_elapsed_time_verbose_months(months: float) -> str:
    """
    Returns a string describing the specified number of months in
    conversational tone, which means that it can describe time in terms
    of months or years.

    :param months: The time period in months.
    """

    if months < 0.0 + _CLOSE_TO_VALUE:
        return "0 months"

    if 1.0 - _CLOSE_TO_VALUE <= months <= 1.0 + _CLOSE_TO_VALUE:
        return "1 month"

    if months <= MONTHS_PER_YEAR * _UNIT_THRESHOLD:
        return '{:3.1f} months'.format(months)

    return to_elapsed_time_verbose_years(months / MONTHS_PER_YEAR)


# =========================================================================
# to_elapsed_time_verbose_years
# =========================================================================

def to_elapsed_time_verbose_years(years: float) -> str:
    """
    Returns a string describing the specified number of years in
    conversational tone.

    :param years: The time period in years.
    """

    if years < 0.0 + _CLOSE_TO_VALUE:
        return "0 years"

    if 1.0 - _CLOSE_TO_VALUE <= years <= 1.0 + _CLOSE_TO_VALUE:
        return "1 year"

    return '{:3.1f} years'.format(years)


# =========================================================================
# to_hex_ascii
# =========================================================================

def to_hex_ascii(value: str) -> str:
    """
    Returns the value of the string with the bytes converted to hex-ASCII
    characters.

    :param value: The string to convert.
    :return: The value of the given string converted to hex-ASCII
        characters.
    @raises ValueError: if any of the character values are > 255
    """

    snippets: list = []
    for char in value:
        if ord(char) > _MAX_HEX_ASCII_VALUE:
            raise ValueError(
                'The character 0x{:04X} is outside the ASCII range'
                .format(ord(char)))
        snippets.append('{:02X}'.format(ord(char)))
    return ''.join(snippets)


# =========================================================================
# to_regex_or_expression
# =========================================================================

def to_regex_or_expression(terms) -> str:
    """
    Returns a string containing a regular expression constructed by ORing
    together (with the pipe '|', of course) the stringified values of the
    given terms and enclosing the whole expression with a non-capture
    group ('(?:' ... ')'); in addition, all of the values are escaped,
    as appropriate, to literal values.

    If terms is empty then an empty string is returned.

    If terms contains only one element then only that element is returned
    without the non-capture group syntax; in addition, if terms is a set
    then the method sorts the terms lexicographically
    (for ease of unit testing).

    :param terms: A list or set of terms to combine.
    :return: The regular expression.
    """

    if len(terms) == 0:
        return ""

    if len(terms) == 1:
        for term in terms:
            return add_escape_sequences_for_regex(stringify(term))

    components = [add_escape_sequences_for_regex(stringify(term))
                  for term in terms]

    if isinstance(terms, set):
        components.sort()

    return '(?:' + '|'.join(components) + ')'
