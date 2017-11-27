"""
Created on January 27, 2017

@author: John Jackson
"""

import logging
import unittest
from unittest import mock
from unittest.mock import call

from kojak.core.test_logger import TestLogger
from test_utilities.test_utilities import verify_mock_calls

logging.basicConfig(level=logging.DEBUG)


PATCH_LOGGING = 'kojak.core.test_logger.logging'
PATCH_TIME = 'kojak.core.test_logger.time'


###############################################################################
# TEST TestLogger
###############################################################################

class TestTestLogger(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):
        x = TestLogger()

        self.assertIsNone(x._feature_stats)
        self.assertEqual(x._last_begin_header, '')
        self.assertEqual(x._last_feature_header, '')
        self.assertEqual(x._last_given_header, '')
        self.assertEqual(x._last_scenario_header, '')
        self.assertEqual(x._last_section_header, '')
        self.assertEqual(x._last_then_header, '')
        self.assertEqual(x._last_when_header, '')
        self.assertEqual(x._mode, TestLogger.Mode.PROD)
        self.assertIsNotNone(x._run_stats)
        self.assertFalse(x._suppress_info_output)

    # =========================================================================
    # METHOD - begin_feature
    # =========================================================================

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_begin_feature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # Populate the lower headers so that we can see that the next call
        # to begin_feature clears them.  Clear the list of mocked calls
        # so that we don't have to add verify statements; we'll test these
        # methods in their own test cases.
        x.begin_scenario("Scenario")
        x.begin_section("Section")
        x.begin_given("Given")
        x.begin_when("When")
        # Discard calls from setup
        mock_logging.mock_calls = []

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: Feature"),
            call.info(" Scenario: Scenario"),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_feature('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE unknown"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_given
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_begin_given(self, mock_logging):
        x = TestLogger()

        x.begin_given("Given")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: Given"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # Populate the lower headers so that we can see that the next call
        # to begin_given clears them. Clear the list of mocked calls so that
        # we don't have to add verify statements; we'll test these methods
        # in their own test cases.
        x.begin_when("When")
        # Discard calls from setup
        mock_logging.mock_calls = []

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_given('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_scenario
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_begin_scenario(self, mock_logging):
        x = TestLogger()

        x.begin_scenario("Scenario")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: Scenario"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # Populate the lower headers so that we can see that the next call
        # to begin_scenario clears them. Clear the list of mocked calls
        # so that we don't have to add verify statements; we'll test these
        # methods in their own test cases.
        x.begin_section("Section")
        x.begin_given("Given")
        x.begin_when("When")
        # Discard calls from setup
        mock_logging.mock_calls = []

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: Scenario"),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_scenario('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_section
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_begin_section(self, mock_logging):
        x = TestLogger()

        x.begin_section("Section")
        # begin_section doesn't print anything.
        expected_calls = [
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # Populate the lower headers so that we can see that the next call
        # to begin_scenario clears them. Clear the list of mocked calls
        # so that we don't have to add verify statements; we'll test these
        # methods in their own test cases.
        x.begin_given("Given")
        x.begin_when("When")
        # Discard calls from setup
        mock_logging.mock_calls = []

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_section('')
        # begin_section doesn't print anything.
        expected_calls = [
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_then
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_begin_then(self, mock_logging):
        x = TestLogger()

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_when
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_begin_when(self, mock_logging):
        x = TestLogger()

        x.begin_when("When")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: When"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then("Then")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_when('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.begin_then('')
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - begin_feature
    # =========================================================================

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_end_feature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # end_feature will re-enable info output.
        x.set_suppress_info_output(True)
        x.info("This message should be suppressed")
        expected_calls = [
            call.info("Disabling info output"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info("Enabling info output"),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info("This message should not be suppressed")
        expected_calls = [
            call.info("This message should not be suppressed"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # end_feature will re-enable info output.
        x.set_suppress_info_output(True)
        x.info("This message should be suppressed")
        expected_calls = [
            call.info("Disabling info output"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        # With no active feature, end_feature does nothing but disable info suppression
        x.end_feature()
        expected_calls = [
            call.info("Enabling info output"),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info("This message should not be suppressed")
        expected_calls = [
            call.info("This message should not be suppressed"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - fail_test
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_fail_test__literal_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg", x.fail_test("testmsg"))
        expected_calls = [
            call.error("-FAIL- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_fail_test__format_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg testmsg2", x.fail_test("testmsg {}", "testmsg2"))
        expected_calls = [
            call.error("-FAIL- : testmsg testmsg2"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_fail_test__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        # Discard calls from setup
        mock_logging.mock_calls = []

        self.assertEqual("testmsg", x.fail_test("testmsg"))
        expected_calls = [
            call.error("-FAIL- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: FAIL"),
            call.info(''),
            call.info("         1 : Total tests"),
            call.info("         1 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Failures  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: FAIL"),
            call.info(''),
            call.info("         1 : Total tests"),
            call.info("         1 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Failures  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - get_mode
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_get_mode(self, mock_logging):
        x = TestLogger()

        # Check initial value
        self.assertIs(TestLogger.Mode.PROD, x.get_mode())

        # Change to different value
        self.assertIs(TestLogger.Mode.PROD, x.set_mode(TestLogger.Mode.TEST))
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)
        self.assertIs(TestLogger.Mode.TEST, x.get_mode())

        # Change to default value
        self.assertIs(TestLogger.Mode.TEST, x.set_mode())
        expected_calls = [
            call.info("The logging mode is now PROD"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)
        self.assertIs(TestLogger.Mode.PROD, x.get_mode())

        # Set to same value
        self.assertIs(TestLogger.Mode.PROD, x.set_mode(TestLogger.Mode.PROD))
        expected_calls = [
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)
        self.assertIs(TestLogger.Mode.PROD, x.get_mode())

    # =========================================================================
    # METHOD - info
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_info__no_parameters(self, mock_logging):
        x = TestLogger()

        x.info()
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info__object__None(self, mock_logging):
        """
        Test with None parameter
        """
        x = TestLogger()

        x.info(None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info__object__True(self, mock_logging):
        """
        Test with boolean parameter
        """
        x = TestLogger()

        x.info(True)
        expected_calls = [
            call.info("True"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info__literal(self, mock_logging):
        """
        Test with single parameter
        """
        x = TestLogger()

        x.info("Hello {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info__format(self, mock_logging):
        """
        Test with format and value parameter
        """
        x = TestLogger()

        x.info("Hello {}", "Goodbye")
        expected_calls = [
            call.info("Hello Goodbye"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - info_list
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_info_list(self, mock_logging):
        x = TestLogger()

        x.info_list(["line1", "line2", "line3"], "line dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN line dump  =========="),
            call.info(''),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(''),
            call.info("==========  END line dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_list__no_title(self, mock_logging):
        x = TestLogger()

        x.info_list(["line1", "line2", "line3"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - info_mode
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_info_mode(self, mock_logging):
        """
        Test with no parameters
        """
        x = TestLogger()

        x.info_mode(TestLogger.Mode.PROD)
        x.info_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode(TestLogger.Mode.PROD)
        x.info_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_mode__object__None(self, mock_logging):
        """
        Test with None parameter
        """
        x = TestLogger()

        x.info_mode(TestLogger.Mode.PROD, None)
        x.info_mode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode(TestLogger.Mode.PROD, None)
        x.info_mode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_mode__object__True(self, mock_logging):
        """
        Test with boolean parameter
        """
        x = TestLogger()

        x.info_mode(TestLogger.Mode.PROD, True)
        x.info_mode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("True"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode(TestLogger.Mode.PROD, True)
        x.info_mode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("False"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_mode__literal(self, mock_logging):
        """
        Test with single parameter
        """
        x = TestLogger()

        x.info_mode(TestLogger.Mode.PROD, "Hello {}")
        x.info_mode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode(TestLogger.Mode.PROD, "Hello {}")
        x.info_mode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Goodbye {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_mode__format(self, mock_logging):
        """
        Test with format and value parameter
        """
        x = TestLogger()

        x.info_mode(TestLogger.Mode.PROD, "Hello {}", "there")
        x.info_mode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Hello there"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode(TestLogger.Mode.PROD, "Hello {}", "there")
        x.info_mode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Goodbye y'all"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - info_mode_list
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_info_mode_list(self, mock_logging):
        x = TestLogger()

        x.info_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        x.info_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN prod dump  =========="),
            call.info(''),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(''),
            call.info("==========  END prod dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        x.info_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN test dump  =========="),
            call.info(''),
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
            call.info(''),
            call.info("==========  END test dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_info_mode_list__no_title(self, mock_logging):
        x = TestLogger()

        x.info_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        x.info_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.info_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        x.info_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - pass_test
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_pass_test__literal__WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg", x.pass_test("testmsg"))
        expected_calls = [
            call.info(" PASS  : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_pass_test__format__WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg testmsg2", x.pass_test("testmsg {}", "testmsg2"))
        expected_calls = [
            call.info(" PASS  : testmsg testmsg2"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_pass_test__literal__WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        # Discard calls from setup.
        mock_logging.mock_calls = []

        self.assertEqual("testmsg", x.pass_test("testmsg"))
        expected_calls = [
            call.info(" PASS  : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         1 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         1 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - print_banner
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg")
        expected_calls = [
            call.info("testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1)
        expected_calls = [
            call.info(''),
            call.info("testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2)
        expected_calls = [
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before__banners_after(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2, 3)
        expected_calls = [
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("testmsg"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before__banners_after__blanks_after(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2, 3, 4)
        expected_calls = [
            call.info(''),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("testmsg"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before__banners_after__blanks_after__banner0(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2, 3, 4, '')
        expected_calls = [
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before__banners_after__blanks_after__banner1(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2, 3, 4, "X")
        expected_calls = [
            call.info(''),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("testmsg"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__message__blanks_before__banners_before__banners_after__blanks_after__banner3(self, mock_logging):
        x = TestLogger()

        x.print_banner("testmsg", 1, 2, 3, 4, "Xyz")
        expected_calls = [
            call.info(''),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("testmsg"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info(''),
            call.info(''),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_banner__long_message(self, mock_logging):
        x = TestLogger()

        x.print_banner("ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXY", 0, 1, 1, 0)
        expected_calls = [
            call.info("#############################################################################################################################"),
            call.info("ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXY"),
            call.info("#############################################################################################################################"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - print_header_begin
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_print_header_begin__literal(self, mock_logging):
        x = TestLogger()

        x.print_header_begin("testmsg")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN testmsg  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_begin("hello")
        expected_calls = [
            call.info(''),
            call.info("==========  END testmsg  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN hello  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_end()
        expected_calls = [
            call.info(''),
            call.info("==========  END hello  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_begin("serendipity")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN serendipity  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_begin('')
        expected_calls = [
            call.info(''),
            call.info("==========  END serendipity  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN -unspecified-  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_end()
        expected_calls = [
            call.info(''),
            call.info("==========  END -unspecified-  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_header_begin__format(self, mock_logging):
        x = TestLogger()

        x.print_header_begin("testmsg {} {}", "A", 1)
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN testmsg A 1  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.print_header_end()
        expected_calls = [
            call.info(''),
            call.info("==========  END testmsg A 1  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - print_header_end
    # =========================================================================

    def test_print_header_end(self):
        pass
        # Tested with print_header_begin

    # =========================================================================
    # METHOD - print_header_dash
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_print_header_dash__literal(self, mock_logging):
        x = TestLogger()

        x.print_header_dash("testmsg")
        expected_calls = [
            call.info(''),
            call.info("-----  testmsg  -----"),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_header_dash__format(self, mock_logging):
        x = TestLogger()

        x.print_header_dash("testmsg {} {}", "A", 1)
        expected_calls = [
            call.info(''),
            call.info("-----  testmsg A 1  -----"),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - print_header_equal
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_print_header_equal__literal(self, mock_logging):
        x = TestLogger()

        x.print_header_equal("testmsg")
        expected_calls = [
            call.info(''),
            call.info("===================================================================================================="),
            call.info("testmsg"),
            call.info("===================================================================================================="),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_header_equal__format(self, mock_logging):
        x = TestLogger()

        x.print_header_equal("testmsg {} {}", "A", 1)
        expected_calls = [
            call.info(''),
            call.info("===================================================================================================="),
            call.info("testmsg A 1"),
            call.info("===================================================================================================="),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - print_header_plus
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_print_header_plus__literal(self, mock_logging):
        x = TestLogger()

        x.print_header_plus("testmsg")
        expected_calls = [
            call.info(''),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
            call.info("testmsg"),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_print_header_plus__format(self, mock_logging):
        x = TestLogger()

        x.print_header_plus("testmsg {} {}", "A", 1)
        expected_calls = [
            call.info(''),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
            call.info("testmsg A 1"),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - set_mode
    # =========================================================================

    def test_set_mode(self):
        pass
        # Tested with get_mode

    # =========================================================================
    # METHOD - set_suppress_info_output
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_set_suppress_info_output__info(self, mock_logging):
        x = TestLogger()

        x.info("line1")
        x.set_suppress_info_output(True)
        x.info("line2")
        x.set_suppress_info_output(False)
        x.info("line3")
        expected_calls = [
            call.info("line1"),
            call.info("Disabling info output"),
            call.info("Enabling info output"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_set_suppress_info_output__tell(self, mock_logging):
        x = TestLogger()

        x.tell("line1")
        x.set_suppress_info_output(True)
        x.tell("line2")
        x.set_suppress_info_output(False)
        x.tell("line3")
        expected_calls = [
            call.info("line1"),
            call.info("Disabling info output"),
            call.info("line2"),
            call.info("Enabling info output"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - tell
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_tell(self, mock_logging):
        """
        Test with no parameters
        """
        x = TestLogger()

        x.tell()
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell__object__None(self, mock_logging):
        """
        Test with None parameter
        """
        x = TestLogger()

        x.tell(None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell__object__True(self, mock_logging):
        """
        Test with boolean parameter
        """
        x = TestLogger()

        x.tell(True)
        expected_calls = [
            call.info("True"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell__literal(self, mock_logging):
        """
        Test with single parameter
        """
        x = TestLogger()

        x.tell("Hello {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell__format(self, mock_logging):
        """
        Test with format and value parameter
        """
        x = TestLogger()

        x.tell("Hello {}", "Goodbye")
        expected_calls = [
            call.info("Hello Goodbye"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - tell_list
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_tell_list(self, mock_logging):
        x = TestLogger()

        x.tell_list(["line1", "line2", "line3"], "line dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN line dump  =========="),
            call.info(''),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(''),
            call.info("==========  END line dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_list__no_title(self, mock_logging):
        x = TestLogger()

        x.tell_list(["line1", "line2", "line3"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - tell_mode
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode(self, mock_logging):
        """
        Test with no parameters
        """
        x = TestLogger()

        x.tell_mode(TestLogger.Mode.PROD)
        x.tell_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode(TestLogger.Mode.PROD)
        x.tell_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode__object__None(self, mock_logging):
        """
        Test with None parameter
        """
        x = TestLogger()

        x.tell_mode(TestLogger.Mode.PROD, None)
        x.tell_mode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode(TestLogger.Mode.PROD, None)
        x.tell_mode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode__object__True(self, mock_logging):
        """
        Test with boolean parameter
        """
        x = TestLogger()

        x.tell_mode(TestLogger.Mode.PROD, True)
        x.tell_mode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("True"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode(TestLogger.Mode.PROD, True)
        x.tell_mode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("False"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode__literal(self, mock_logging):
        """
        Test with single parameter
        """
        x = TestLogger()

        x.tell_mode(TestLogger.Mode.PROD, "Hello {}")
        x.tell_mode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode(TestLogger.Mode.PROD, "Hello {}")
        x.tell_mode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Goodbye {}"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode__format(self, mock_logging):
        """
        Test with format and value parameter
        """
        x = TestLogger()

        x.tell_mode(TestLogger.Mode.PROD, "Hello {}", "there")
        x.tell_mode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Hello there"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode(TestLogger.Mode.PROD, "Hello {}", "there")
        x.tell_mode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Goodbye y'all"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - tell_mode_list
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode_list(self, mock_logging):
        x = TestLogger()

        x.tell_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        x.tell_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN prod dump  =========="),
            call.info(''),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(''),
            call.info("==========  END prod dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        x.tell_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(''),
            call.info("==========  BEGIN test dump  =========="),
            call.info(''),
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
            call.info(''),
            call.info("==========  END test dump  =========="),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_tell_mode_list__no_title(self, mock_logging):
        x = TestLogger()

        x.tell_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        x.tell_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.set_mode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.tell_mode_list(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        x.tell_mode_list(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - warn
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_warn__literal_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg", x.warn("testmsg"))
        expected_calls = [
            call.warning("-WARN- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_warn__format_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg testmsg2", x.warn("testmsg {}", "testmsg2"))
        expected_calls = [
            call.warning("-WARN- : testmsg testmsg2"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_warn__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        # Discard calls from setup
        mock_logging.mock_calls = []

        self.assertEqual("testmsg", x.warn("testmsg"))
        expected_calls = [
            call.warning("-WARN- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         1 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Warnings  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         1 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Warnings  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - warn_exception
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_warn_exception(self, mock_logging):

        x = TestLogger()

        e = TypeError("testmsg")
        x.warn_exception(e)
        expected_calls = [
            call.exception(e),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - warn_once
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_warn_once__literal_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg", x.warn_once("testmsg"))
        self.assertEqual("testmsg", x.warn_once("testmsg"))
        expected_calls = [
            call.warning("-WARN- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_warn_once__format_WithoutFeature(self, mock_logging):
        x = TestLogger()

        self.assertEqual("testmsg testmsg2", x.warn_once("testmsg {}", "testmsg2"))
        self.assertEqual("testmsg testmsg2", x.warn_once("testmsg {}", "testmsg2"))
        expected_calls = [
            call.warning("-WARN- : testmsg testmsg2"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_warn_once__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        # Discard calls from setup
        mock_logging.mock_calls = []

        self.assertEqual("testmsg", x.warn_once("testmsg"))
        self.assertEqual("testmsg", x.warn_once("testmsg"))
        expected_calls = [
            call.warning("-WARN- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         2 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Warnings  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         2 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Warnings  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    # =========================================================================
    # METHOD - workaround
    # =========================================================================

    @mock.patch(PATCH_LOGGING)
    def test_workaround__literal_WithoutFeature(self, mock_logging):
        x = TestLogger()

        x.workaround("testmsg")
        x.workaround("testmsg")
        expected_calls = [
            call.warning("-WORK- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_LOGGING)
    def test_workaround__format_WithoutFeature(self, mock_logging):
        x = TestLogger()

        x.workaround("testmsg {}", "testmsg2")
        x.workaround("testmsg {}", "testmsg2")
        expected_calls = [
            call.warning("-WORK- : testmsg testmsg2"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

    @mock.patch(PATCH_TIME)
    @mock.patch(PATCH_LOGGING)
    def test_workaround__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        x = TestLogger()

        x.begin_feature("Feature")
        # Discard calls from setup
        mock_logging.mock_calls = []

        x.workaround("testmsg")
        x.workaround("testmsg")
        expected_calls = [
            call.warning("-WORK- : testmsg"),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)

        x.end_feature()
        expected_calls = [
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         2 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Workarounds  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(''),
            call.info("RESULT: PASS"),
            call.info(''),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         2 : Total workarounds"),
            call.info(''),
            call.info("Elapsed time: 0 seconds"),
            call.info(''),
            call.info("-----  Unique Workarounds  -----"),
            call.info(''),
            call.info("testmsg"),
            call.info(''),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(''),
            call.info(''),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(''),
            call.info(''),
        ]
        verify_mock_calls(self, mock_logging.mock_calls, expected_calls)


if __name__ == '__main__':
    unittest.main()
