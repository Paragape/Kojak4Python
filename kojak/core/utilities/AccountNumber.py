"""
Created on February 12, 2017

@author: John Jackson
"""

from kojak.core.TestLogger import TestLogger
from kojak.core.utilities.AccountNumberMasker import AccountNumberMasker


class AccountNumber:
    """
    This class represents a credit-card or bank account number and associated numbers, such as card verification value and routing number.
    """

    ####################################################################################################
    # CONSTANTS - PUBLIC
    ####################################################################################################

    # Defines the default length of the Card Verification Value, in digits.
    DEFAULT_CVV_LENGTH: int = 3

    ####################################################################################################
    # METHODS
    ####################################################################################################

    # ====================================================================================================
    # CONSTRUCTOR
    # ====================================================================================================

    def __init__(self,
                 clear_text_account_number: str,
                 bank_display_name='',
                 bank_name='',
                 cvv='',
                 cvv_bad='',
                 cvv_length=-1,
                 masker=None,
                 routing_number='',
                 use_bad_cvv=False):
        """
        Creates a new AccountNumber with the given values.  The method assigns the value of <b>cvv</b> plus one as the bad CVV.
        @param clear_text_account_number The clear-text account number to set.
        @param bank_display_name An optional bank name to appear in your test log files.
        @param bank_name An optional bank name that you might include in service requests.
        @param cvv An optional card verification value; if you omit this parameter, the cvv is set to the last three digits of the account number.
        @param cvv_bad The CVV to use when C{use_bad_cvv=True}; if you omit this parameter, the bad cvv is set to the value of cvv+1, wrapped to zero if necessary.
        @param cvv_length An optional value specifying the length of the card verification value. If you also specify cvv then cvv_length is ignored.
        @param masker An optional Masker that knows how to match the masked card number values that appear in your test log files.
        @param routing_number An optional routing number to set.
        @param use_bad_cvv If set to True, C{getCVV()} returns a bad CVV.
        """

        # Holds the name of the bank associated with this account number; this name is appropriate for logging in log files.
        self._bank_display_name: str = bank_display_name

        # Holds the name of the bank associated with this account number; this name is appropriate for identifying the bank in service requests.
        self._bank_name: str = bank_name

        # Holds the clear-text account number.
        self._clear_text_account_number: str = clear_text_account_number

        # Holds the card validation value associated with this account number.
        self._cvv: str = cvv

        # Holds an incorrect card validation value associated with this account number.
        self._cvv_bad: str = cvv_bad

        # Holds the length of the card validation value associated with this account number.
        self._cvv_length: int = len(cvv) if len(cvv) > 0 else cvv_length if cvv_length >= 0 else self.DEFAULT_CVV_LENGTH if len(clear_text_account_number) > self.DEFAULT_CVV_LENGTH else len(clear_text_account_number)

        # Holds the AccountNumberMasker that knows how to mask the account number.  For PCI compliance you must
        # mask account numbers that appear in log files and this masker knows how to mimic what appears in your test log files.
        self._masker: AccountNumberMasker = masker

        # Holds the routing number; this applies to bank accounts rather thn card accounts.
        self._routing_number: str = routing_number

        # Determines whether method C{getCVV()} should return good or bad card verification values.
        self._use_bad_cvv: bool = use_bad_cvv

        # Calculate a cvv if no cvv was given explicitly.
        if len(cvv) == 0:
            if self._cvv_length <= 0:
                pass
            elif len(clear_text_account_number) <= self._cvv_length:
                cvv = clear_text_account_number
            else:
                cvv = clear_text_account_number[len(clear_text_account_number)-self._cvv_length:]

        # Set the final value of _cvv, _cvv_length, and _cvv_bad.
        self.setCVV(cvv, cvv_bad)

    # ====================================================================================================
    # __str__
    # ====================================================================================================

    def __str__(self):
        return "'%s' (cvv='%s' cvv_bad='%s' masked='%s' bank_name='%s' bank_display_name='%s' routing_number='%s')" % (
            self._clear_text_account_number,
            self._cvv,
            self._cvv_bad,
            self.getMaskedNumber(),
            self._bank_name,
            self._bank_display_name,
            self._routing_number
        )

    # ====================================================================================================
    # copy
    # ====================================================================================================

    def copy(self) -> 'AccountNumber':
        """
        Creates a copy of this AccountNumber.
        """

        new = AccountNumber(
            clear_text_account_number=self._clear_text_account_number,
            bank_display_name=self._bank_display_name,
            bank_name=self._bank_name,
            cvv=self._cvv,
            cvv_bad=self._cvv_bad,
            cvv_length=self._cvv_length,
            masker=self._masker,
            routing_number=self._routing_number,
            use_bad_cvv=self._use_bad_cvv
        )

        return new

    # ====================================================================================================
    # getBankDisplayName
    # ====================================================================================================

    def getBankDisplayName(self) -> str:
        """
        Returns the name of the bank associated with this account number; this name should be appropriate for logging in log files.
        """

        return self._bank_display_name

    # ====================================================================================================
    # getBankName
    # ====================================================================================================

    def getBankName(self) -> str:
        """
        Returns the name of the bank associated with this account number; this name should be appropriate for identifying the bank in service requests.
        """

        return self._bank_name

    # ====================================================================================================
    # getClearTextNumber
    # ====================================================================================================

    def getClearTextNumber(self) -> str:
        """
        Returns the clear-text account number.
        """

        return self._clear_text_account_number

    # ====================================================================================================
    # getCVV
    # ====================================================================================================

    def getCVV(self) -> str:
        """
        Returns the card validation value associated with this account number.  However, if you have previously called
        C{useBadCVV} with True then the method returns an incorrect card validation value.
        By default, the CVV value is set to the last three digits of the clear-text account number.
        """

        return self._cvv_bad if self._use_bad_cvv else self._cvv

    # ====================================================================================================
    # getCVVBad
    # ====================================================================================================

    def getCVVBad(self) -> str:
        """
        Returns an incorrect card validation value associated with this account number.
        """

        return self._cvv_bad

    # ====================================================================================================
    # getCVVLength
    # ====================================================================================================

    def getCVVLength(self) -> int:
        """
        Returns the length of the card validation value associated with this account number.
        """

        return self._cvv_length

    # ====================================================================================================
    # getLastN
    # ====================================================================================================

    def getLastN(self, n: int) -> str:
        """
        Returns the last N digits of the clear-text account number.
        @param n The number of digits to return.
        @return A string containing the last N digits of the clear-text account number.
        """

        n = 0 if n < 0 else n
        return self._clear_text_account_number if len(self._clear_text_account_number) < n else self._clear_text_account_number[len(self._clear_text_account_number) - n:]

    # ====================================================================================================
    # getMaskedNumber
    # ====================================================================================================

    def getMaskedNumber(self) -> str:
        """
        Returns the clear-text account number masked according to the rules of this AccountNumber's masker.
        If this AccountNumber has no masker, the method returns the clear-text account number.
        """

        return self._clear_text_account_number if self._masker is None else self._masker.maskNumber(self._clear_text_account_number)

    # ====================================================================================================
    # getMasker
    # ====================================================================================================

    def getMasker(self) -> AccountNumberMasker:
        """
        Returns the AccountNumberMasker associated with this AccountNumber.  For PCI compliance you must
        mask account numbers that appear in log files and this masker knows how to mimic what appears in your test log files.
        """

        return self._masker

    # ====================================================================================================
    # getRoutingNumber
    # ====================================================================================================

    def getRoutingNumber(self) -> str:
        """
        Returns the routing number.
        """

        return self._routing_number

    # ====================================================================================================
    # _normalizeCVV
    # ====================================================================================================

    @staticmethod
    def _normalizeCVV(cvv: str, length: int) -> str:
        """
        Returns the given CVV normalized to the given length.
        If the length of the given CVV < B{length}, then zeroes are prepended to make it the given B{length}.
        If the length of the given CVV > B{length} then the given cvv is truncated to the last B{length} characters of the given B{cvv}.
        @param cvv The CVV to normalize.
        @param length The desired length of the normalized CVV.
        @return The normalized CVV.
        """
        if len(cvv) < length:
            # Zerofill to the correct length.
            return ('0' * (length - len(cvv))) + cvv
        elif len(cvv) > length:
            # Handles case where '999', for example, increments to '1000'
            return cvv[len(cvv) - length:]
        else:
            return cvv

    # ====================================================================================================
    # setClearTextNumber
    # ====================================================================================================

    def setClearTextNumber(self, clear_text_account_number: str) -> None:
        """
        Sets the clear-text account number and calls C{setCVV()} with the last N digits of the account number
        where N is the cvv length established at the AccountNumber's construction.
        """

        self._clear_text_account_number = clear_text_account_number
        cvv: str = clear_text_account_number if len(clear_text_account_number) <= self._cvv_length else clear_text_account_number[len(clear_text_account_number)-self._cvv_length:]
        self.setCVV(cvv)

    # ====================================================================================================
    # setCVV
    # ====================================================================================================

    def setCVV(self, cvv: str, cvv_bad: str = '') -> None:
        """
        Sets the card validation value associated with this account number as well as the incorrect card validation value.
        The incorrect CVV is set to the value of the correct CVV plus 1 (wrapping to zero if necessary.)  However, if you
        specify a null, blank, or non-numeric CVV then the incorrect CVV is set to null.
        @param cvv The CVV value to set.
        @param cvv_bad The bad CVV value to set, or the empty string to set the default CVV value, which is the CVV value plus one, wrapped to zero if necessary.
        """

        cvv_length: int = len(cvv)
        cvv_bad_length: int = len(cvv_bad)
        if cvv_length > 0 and cvv_bad_length == 0:
            cvv = self._normalizeCVV(cvv, cvv_length)
            try:
                # cvv_bad = cvv + 1
                cvv_bad = self._normalizeCVV(str(int(cvv)+1), cvv_length)
            except ValueError:
                TestLogger().warn("Exception encountered trying to create the bad CVV for '%s'", cvv)

        self._cvv = cvv
        self._cvv_bad = cvv_bad
        self._cvv_length = cvv_length

    # ====================================================================================================
    # setRoutingNumber
    # ====================================================================================================

    def setRoutingNumber(self, routing_number: str) -> None:
        """
        Sets the routing number.
        @param routing_number The routing number to set.
        """

        self._routing_number = routing_number

    # ====================================================================================================
    # useBadCVV
    # ====================================================================================================

    def useBadCVV(self, use_bad_cvv: bool) -> None:
        """
        Sets whether C{getCVV()} returns the correct or an incorrect card verification value.  This condition is set False by default.
        @param use_bad_cvv The condition to set; true instructs C{getCVV()} to return a bad CVV value.
        """

        self._use_bad_cvv = use_bad_cvv
