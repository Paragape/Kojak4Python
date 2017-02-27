"""
Created on February 12, 2017

@author: John Jackson
"""


class AccountNumberMasker:
    """
    This class contains specific instructions on how to mask an account number. For PCI compliance, you need to mask account numbers that appear in log
    files. You create a subclass to provide specific instructions on how the AccountNumber class should generate masked account numbers that match your
    log files so that your log files can be verified.
    """

    ####################################################################################################
    # METHODS
    ####################################################################################################

    # ====================================================================================================
    # CONSTRUCTOR
    # ====================================================================================================

    def __init__(self, first_m=4, last_n=4, mask_character='*'):
        """
        Creates a new AccountNumberMasker that leaves the specified first M and last N digits clear.
        @param first_m The count of leading digits to leave in clear text; the default is 4.
        @param last_n The count of trailing digits to leave in clear text; the default is 4.
        @param mask_character The character to use for masking the middle digits; the default is '*'.
        """

        self._first_m: int = first_m if first_m >= 0 else 0
        self._last_n: int = last_n if last_n >= 0 else 0
        self._mask_character: str = mask_character if len(mask_character) == 1 else '*' if len(mask_character) == 0 else mask_character[0]

    # ====================================================================================================
    # maskNumber
    # ====================================================================================================

    def maskNumber(self, number: str) -> str:
        """
        Returns a masked version of the specified number according to the criteria provided in the constructor.
        If the number is null or its length is <= B{firstM+lastN} then the number is returned as-is.
        <p>
        If your log files mask numbers using this straight-forward technique then your subclass can use this method to mask your numbers.
        @param number The number to mask.
        @return The masked number.
        """

        if len(number) <= self._first_m + self._last_n:
            return number

        mask_length: int = len(number) - self._first_m - self._last_n
        return number[:self._first_m] + (self._mask_character * mask_length) + number[len(number)-self._last_n:]

    # ====================================================================================================
    # __str__
    # ====================================================================================================

    def __str__(self):
        return "Mask: %d-%s-%d" % (self._first_m, self._mask_character, self._last_n)
