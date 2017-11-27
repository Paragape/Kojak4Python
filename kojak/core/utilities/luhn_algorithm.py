"""
Created on November 18, 2017

This module provides methods for calculating and verifying with the LUHN
checksum algorithm.

@author: John Jackson
"""

from typing import Optional

###############################################################################
# CONSTANTS
###############################################################################

# Use these tables to "luhn-divide" and "luhn-multiply" a digit by two.
# When the Luhn algorithm multiplies a digit by two, the result is the product
# itself for single-digit products (2*3=6 => 6) and the sum of the digits
# of the product for two-digit products (2*6=12 => 1+2 => 3).  Division by two
# does the reverse.

# Index into this list with a single-digit value (0-9) to get back the
# single-digit value that represents the value of the index divided by 2.

_LUHN_DIVIDE_BY_TWO = (0, 5, 1, 6, 2, 7, 3, 8, 4, 9)

# Index into this table with a single-digit value (0-9) to get back the
# single-digit value that represents the value of the index multiplied by 2.

_LUHN_MULTIPLY_BY_TWO = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)


###############################################################################
# METHODS
###############################################################################


# =============================================================================
# add_checksum
# =============================================================================

def add_checksum(number_string: Optional[str] = None) -> str:
    """
    Returns the completed number string with the LUHN checksum appended.

    :param number_string: The number string, less the checksum digit.
    """

    return '0' if number_string is None \
        else number_string + str(get_check_digit(number_string))


# =============================================================================
# add_prefix
# =============================================================================

def add_prefix(
        prefix: Optional[str] = None,
        luhn_number_string: Optional[str] = None) -> str:
    """
    Prepends the specified prefix plus an adjustment digit to a LUHN number
    string while preserving the original LUHN checksum digit. For example,
    if you specify the prefix "77" and the number string "4588883200009190"
    then the method returns the string "7784588883200009190"; note that an "8"
    was inserted in between in order to preserve the original number's
    checksum. If you specify a null luhn_number_string then the empty string
    is used. If you specify a null or empty prefix, the method returns the
    luhn_number_string as-is.

    :param prefix: The prefix string.
    :param luhn_number_string: The LUHN number string.
    """

    # Just return the prefix if the base number is empty.
    return_value: str = luhn_number_string or ''

    # Just return the base number if the prefix is empty.
    if not prefix:
        return return_value

    # The secret to adding a prefix is that the prefix plus a LUHN checksum
    # must add to zero so as to preserve to original checksum.  If the
    # luhn_number_string has an odd number of digits, then the added checksum
    # would fall into the even (or alternate) position for calculating the
    # checksum, which means the right-most digit of the prefix would fall
    # in the odd position. Similarly, if the luhn_number_string has an even
    # number of digits, then right-most digit of the prefix would fall
    # in the odd position.

    # We set prefix_falls_in_even_position below to TRUE if the right-most
    # digit of the prefix will fall into the even position; don't forget that
    # we'll insert a checksum between the prefix and the luhn_number_string.

    prefix_falls_in_even_position: bool = (len(return_value) % 2) == 0

    # Calculate the check-digit needed for the prefix.

    prefix_digit: int = _get_check_digit(prefix, prefix_falls_in_even_position)

    # If the prefix does not start in an even position then the checksum does
    # start in an even position. In this case, we must halve the value of the
    # checksum since the LUHN algorithm will double it when calculating
    # the checksum.

    if not prefix_falls_in_even_position:
        prefix_digit = _LUHN_DIVIDE_BY_TWO[prefix_digit]

    # Return the final result.
    return prefix + str(prefix_digit) + return_value


# =============================================================================
# get_check_digit
# =============================================================================

def get_check_digit(number_string: Optional[str]) -> int:
    """
    Returns the LUHN check-digit for the specified number string.

    :param number_string: The number string without the check-sum digit.
    """

    return _get_check_digit(number_string, True)


def _get_check_digit(number_string: str, double_down: bool) -> int:
    """
    Returns the LUHN check-digit for the specified number string.

    :param number_string: The number string without the check-sum digit.
    :param double_down: Set this to TRUE if the right-most digit would be a
        double-down digit of the completed LUHN string.
    """

    checksum: int = _get_checksum(number_string, double_down)
    return 10-checksum if checksum > 0 else checksum


# =============================================================================
# get_checksum
# =============================================================================

def get_checksum(number_string: Optional[str]) -> int:
    """
    Returns the LUHN checksum of the specified number string.

    :param number_string: The number string without the check-sum digit.
    """

    return _get_checksum(number_string, True)


def _get_checksum(number_string: str, double_down: bool) -> int:
    """
    Returns the LUHN checksum of the specified number string.

    :param number_string: The number string without the check-sum digit.
    :param double_down: Set this to TRUE if the right-most digit would be a
        double-down digit of the completed LUHN string.
    """

    # Test for exceptional cases.
    if not number_string:
        return 0

    checksum: int = 0
    is_double_down_digit: bool = double_down
    for digit in reversed(number_string):
        n: int = int(digit)
        checksum += _LUHN_MULTIPLY_BY_TWO[n] if is_double_down_digit else n
        is_double_down_digit = not is_double_down_digit

    # The LUHN checksum is just the "ones" digit of the result.
    return checksum % 10


# =============================================================================
# set_checksum
# =============================================================================

def set_checksum(number_string: Optional[str]) -> str:
    """
    Returns the number string with the LUHN checksum computed.

    :param number_string: The number string, including a stand-in checksum
        digit.
    """

    return add_checksum(number_string[:-1] if number_string else None)


# =============================================================================
# verify_checksum
# =============================================================================

def verify_checksum(number_string: Optional[str]) -> bool:
    """
    Returns TRUE if the LUHN checksum digit is correct for the specified
    number string.

    :param number_string: The number string, including a stand-in checksum
        digit.
    """

    # When we call get_checksum with a number string that includes the
    # check-digit then we should get back a checksum of zero.
    return _get_checksum(number_string, False) == 0
