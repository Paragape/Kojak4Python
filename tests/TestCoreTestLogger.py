"""
Created on January 27, 2017

@author: John Jackson
"""

import unittest
from unittest import mock
from unittest.mock import call
import logging
from kojak.core.TestLogger import TestLogger

logging.basicConfig(level=logging.DEBUG)


class TestCoreTestLogger(unittest.TestCase):

    #####################################################################################################
    # METHOD - CONSTRUCTOR
    #####################################################################################################

    def test_method_CONSTRUCTOR(self):
        log = TestLogger()

        self.assertIsNone(log._feature_stats)
        self.assertEqual(log._last_begin_header, "")
        self.assertEqual(log._last_feature_header, "")
        self.assertEqual(log._last_given_header, "")
        self.assertEqual(log._last_scenario_header, "")
        self.assertEqual(log._last_section_header, "")
        self.assertEqual(log._last_then_header, "")
        self.assertEqual(log._last_when_header, "")
        self.assertEqual(log._mode, TestLogger.Mode.PROD)
        self.assertIsNotNone(log._run_stats)
        self.assertFalse(log._suppress_info_output)

    #####################################################################################################
    # METHOD - beginFeature
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # Populate the lower headers so that we can see that the next call to beginFeature clears them.
        # Clear the list of mocked calls so that we don't have to add verify statements; we'll test these methods in their own test cases.
        log.beginScenario("Scenario")
        log.beginSection("Section")
        log.beginGiven("Given")
        log.beginWhen("When")
        mock_logging.mock_calls = []

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: Feature"),
            call.info(" Scenario: Scenario"),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginFeature("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE unknown"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - beginGiven
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginGiven(self, mock_logging):
        log = TestLogger()

        log.beginGiven("Given")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: Given"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # Populate the lower headers so that we can see that the next call to beginGiven clears them.
        # Clear the list of mocked calls so that we don't have to add verify statements; we'll test these methods in their own test cases.
        log.beginWhen("When")
        mock_logging.mock_calls = []

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginGiven("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - beginScenario
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginScenario(self, mock_logging):
        log = TestLogger()

        log.beginScenario("Scenario")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: Scenario"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # Populate the lower headers so that we can see that the next call to beginScenario clears them.
        # Clear the list of mocked calls so that we don't have to add verify statements; we'll test these methods in their own test cases.
        log.beginSection("Section")
        log.beginGiven("Given")
        log.beginWhen("When")
        mock_logging.mock_calls = []

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: Scenario"),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginScenario("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - beginSection
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginSection(self, mock_logging):
        log = TestLogger()

        log.beginSection("Section")
        # beginSection doesn't print anything.
        expected_calls = [
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # Populate the lower headers so that we can see that the next call to beginScenario clears them.
        # Clear the list of mocked calls so that we don't have to add verify statements; we'll test these methods in their own test cases.
        log.beginGiven("Given")
        log.beginWhen("When")
        mock_logging.mock_calls = []

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: Section"),
            call.info(" Given: Given"),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginSection("")
        # beginSection doesn't print anything.
        expected_calls = [
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - beginThen
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginThen(self, mock_logging):
        log = TestLogger()

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - beginWhen
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_beginWhen(self, mock_logging):
        log = TestLogger()

        log.beginWhen("When")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: When"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("Then")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: When"),
            call.info(" Then: Then"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginWhen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.beginThen("")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info(" Feature: "),
            call.info(" Scenario: "),
            call.info(" Section: "),
            call.info(" Given: "),
            call.info(" When: "),
            call.info(" Then: "),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - endFeature
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_endFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("BEGIN FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # endFeature will re-enable info output.
        log.setSuppressInfoOutput(True)
        log.info("This message should be suppressed")
        expected_calls = [
            call.info("Disabling info output"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info("Enabling info output"),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.info("This message should not be suppressed")
        expected_calls = [
            call.info("This message should not be suppressed"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # endFeature will re-enable info output.
        log.setSuppressInfoOutput(True)
        log.info("This message should be suppressed")
        expected_calls = [
            call.info("Disabling info output"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        # With no active feature, endFeature does nothing but disable info suppression
        log.endFeature()
        expected_calls = [
            call.info("Enabling info output"),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.info("This message should not be suppressed")
        expected_calls = [
            call.info("This message should not be suppressed"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - failTest
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_failTest__literal_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar", log.failTest("foobar"))
        expected_calls = [
            call.error("-FAIL- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_failTest__format_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar foobar2", log.failTest("foobar {}", "foobar2"))
        expected_calls = [
            call.error("-FAIL- : foobar foobar2"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_failTest__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        # Discard calls so that we don't have to verify them.
        mock_logging.mock_calls = []

        self.assertEqual("foobar", log.failTest("foobar"))
        expected_calls = [
            call.error("-FAIL- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: FAIL"),
            call.info(""),
            call.info("         1 : Total tests"),
            call.info("         1 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Failures  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: FAIL"),
            call.info(""),
            call.info("         1 : Total tests"),
            call.info("         1 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Failures  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - getMode/SetMode
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_getMode(self, mock_logging):
        log = TestLogger()

        # Check initial value
        self.assertIs(TestLogger.Mode.PROD, log.getMode())

        # Change to different value
        self.assertIs(TestLogger.Mode.PROD, log.setMode(TestLogger.Mode.TEST))
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []
        self.assertIs(TestLogger.Mode.TEST, log.getMode())

        # Change to default value
        self.assertIs(TestLogger.Mode.TEST, log.setMode())
        expected_calls = [
            call.info("The logging mode is now PROD"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []
        self.assertIs(TestLogger.Mode.PROD, log.getMode())

        # Set to same value
        self.assertIs(TestLogger.Mode.PROD, log.setMode(TestLogger.Mode.PROD))
        expected_calls = [
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []
        self.assertIs(TestLogger.Mode.PROD, log.getMode())

    #####################################################################################################
    # METHOD - info
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_info(self, mock_logging):
        """
        Test with no parameters
        """
        log = TestLogger()

        log.info()
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_info_object_None(self, mock_logging):
        """
        Test with None parameter
        """
        log = TestLogger()

        log.info(None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_info_object_True(self, mock_logging):
        """
        Test with boolean parameter
        """
        log = TestLogger()

        log.info(True)
        expected_calls = [
            call.info("True"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_info_literal(self, mock_logging):
        """
        Test with single parameter
        """
        log = TestLogger()

        log.info("Hello {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_info_format(self, mock_logging):
        """
        Test with format and value parameter
        """
        log = TestLogger()

        log.info("Hello {}", "Goodbye")
        expected_calls = [
            call.info("Hello Goodbye"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - infoList
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoList(self, mock_logging):
        log = TestLogger()

        log.infoList(["line1", "line2", "line3"], "line dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN line dump  =========="),
            call.info(""),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(""),
            call.info("==========  END line dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoList_no_title(self, mock_logging):
        log = TestLogger()

        log.infoList(["line1", "line2", "line3"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - infoMode
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoMode(self, mock_logging):
        """
        Test with no parameters
        """
        log = TestLogger()

        log.infoMode(TestLogger.Mode.PROD)
        log.infoMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoMode(TestLogger.Mode.PROD)
        log.infoMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoMode_object_None(self, mock_logging):
        """
        Test with None parameter
        """
        log = TestLogger()

        log.infoMode(TestLogger.Mode.PROD, None)
        log.infoMode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoMode(TestLogger.Mode.PROD, None)
        log.infoMode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoMode_object_True(self, mock_logging):
        """
        Test with boolean parameter
        """
        log = TestLogger()

        log.infoMode(TestLogger.Mode.PROD, True)
        log.infoMode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("True"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoMode(TestLogger.Mode.PROD, True)
        log.infoMode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("False"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoMode_literal(self, mock_logging):
        """
        Test with single parameter
        """
        log = TestLogger()

        log.infoMode(TestLogger.Mode.PROD, "Hello {}")
        log.infoMode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoMode(TestLogger.Mode.PROD, "Hello {}")
        log.infoMode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Goodbye {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoMode_format(self, mock_logging):
        """
        Test with format and value parameter
        """
        log = TestLogger()

        log.infoMode(TestLogger.Mode.PROD, "Hello {}", "there")
        log.infoMode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Hello there"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoMode(TestLogger.Mode.PROD, "Hello {}", "there")
        log.infoMode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Goodbye y'all"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - infoModeList
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoModeList(self, mock_logging):
        log = TestLogger()

        log.infoModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        log.infoModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN prod dump  =========="),
            call.info(""),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(""),
            call.info("==========  END prod dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        log.infoModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN test dump  =========="),
            call.info(""),
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
            call.info(""),
            call.info("==========  END test dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_infoModeList_no_title(self, mock_logging):
        log = TestLogger()

        log.infoModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        log.infoModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.infoModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        log.infoModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - passTest
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_passTest__literal_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar", log.passTest("foobar"))
        expected_calls = [
            call.info(" PASS  : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_passTest__format_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar foobar2", log.passTest("foobar {}", "foobar2"))
        expected_calls = [
            call.info(" PASS  : foobar foobar2"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_passTest__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        # Discard calls so that we don't have to verify them.
        mock_logging.mock_calls = []

        self.assertEqual("foobar", log.passTest("foobar"))
        expected_calls = [
            call.info(" PASS  : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         1 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         1 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - printBanner
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar")
        expected_calls = [
            call.info("foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1)
        expected_calls = [
            call.info(""),
            call.info("foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2)
        expected_calls = [
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before__banners_after(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2, 3)
        expected_calls = [
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("foobar"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before__banners_after__blanks_after(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2, 3, 4)
        expected_calls = [
            call.info(""),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("foobar"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before__banners_after__blanks_after__banner0(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2, 3, 4, "")
        expected_calls = [
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before__banners_after__blanks_after__banner1(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2, 3, 4, "X")
        expected_calls = [
            call.info(""),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("foobar"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__message__blanks_before__banners_before__banners_after__blanks_after__banner3(self, mock_logging):
        log = TestLogger()

        log.printBanner("foobar", 1, 2, 3, 4, "Xyz")
        expected_calls = [
            call.info(""),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("foobar"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info("XyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzXyzX"),
            call.info(""),
            call.info(""),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printBanner__long_message(self, mock_logging):
        log = TestLogger()

        log.printBanner("ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXY", 0, 1, 1, 0)
        expected_calls = [
            call.info("#############################################################################################################################"),
            call.info("ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXY"),
            call.info("#############################################################################################################################"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - printHeaderBegin / printHeaderEnd
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderBegin_literal(self, mock_logging):
        log = TestLogger()

        log.printHeaderBegin("foobar")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN foobar  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderBegin("hello")
        expected_calls = [
            call.info(""),
            call.info("==========  END foobar  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN hello  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderEnd()
        expected_calls = [
            call.info(""),
            call.info("==========  END hello  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderBegin("serendipity")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN serendipity  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderBegin("")
        expected_calls = [
            call.info(""),
            call.info("==========  END serendipity  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN -unspecified-  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderEnd()
        expected_calls = [
            call.info(""),
            call.info("==========  END -unspecified-  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderBegin_format(self, mock_logging):
        log = TestLogger()

        log.printHeaderBegin("foobar {} {}", "A", 1)
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN foobar A 1  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.printHeaderEnd()
        expected_calls = [
            call.info(""),
            call.info("==========  END foobar A 1  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - printHeaderDash
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderDash_literal(self, mock_logging):
        log = TestLogger()

        log.printHeaderDash("foobar")
        expected_calls = [
            call.info(""),
            call.info("-----  foobar  -----"),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderDash_format(self, mock_logging):
        log = TestLogger()

        log.printHeaderDash("foobar {} {}", "A", 1)
        expected_calls = [
            call.info(""),
            call.info("-----  foobar A 1  -----"),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - printHeaderEqual
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderEqual_literal(self, mock_logging):
        log = TestLogger()

        log.printHeaderEqual("foobar")
        expected_calls = [
            call.info(""),
            call.info("===================================================================================================="),
            call.info("foobar"),
            call.info("===================================================================================================="),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderEqual_format(self, mock_logging):
        log = TestLogger()

        log.printHeaderEqual("foobar {} {}", "A", 1)
        expected_calls = [
            call.info(""),
            call.info("===================================================================================================="),
            call.info("foobar A 1"),
            call.info("===================================================================================================="),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - printHeaderPlus
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderPlus_literal(self, mock_logging):
        log = TestLogger()

        log.printHeaderPlus("foobar")
        expected_calls = [
            call.info(""),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
            call.info("foobar"),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_printHeaderPlus_format(self, mock_logging):
        log = TestLogger()

        log.printHeaderPlus("foobar {} {}", "A", 1)
        expected_calls = [
            call.info(""),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
            call.info("foobar A 1"),
            call.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - setMode
    #####################################################################################################

        # Tested with getMode

    #####################################################################################################
    # METHOD - setSuppressInfoOutput
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_setSuppressInfoOutput_info(self, mock_logging):
        log = TestLogger()

        log.info("line1")
        log.setSuppressInfoOutput(True)
        log.info("line2")
        log.setSuppressInfoOutput(False)
        log.info("line3")
        expected_calls = [
            call.info("line1"),
            call.info("Disabling info output"),
            call.info("Enabling info output"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_setSuppressInfoOutput_tell(self, mock_logging):
        log = TestLogger()

        log.tell("line1")
        log.setSuppressInfoOutput(True)
        log.tell("line2")
        log.setSuppressInfoOutput(False)
        log.tell("line3")
        expected_calls = [
            call.info("line1"),
            call.info("Disabling info output"),
            call.info("line2"),
            call.info("Enabling info output"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - tell
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tell(self, mock_logging):
        """
        Test with no parameters
        """
        log = TestLogger()

        log.tell()
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tell_object_None(self, mock_logging):
        """
        Test with None parameter
        """
        log = TestLogger()

        log.tell(None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tell_object_True(self, mock_logging):
        """
        Test with boolean parameter
        """
        log = TestLogger()

        log.tell(True)
        expected_calls = [
            call.info("True"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tell_literal(self, mock_logging):
        """
        Test with single parameter
        """
        log = TestLogger()

        log.tell("Hello {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tell_format(self, mock_logging):
        """
        Test with format and value parameter
        """
        log = TestLogger()

        log.tell("Hello {}", "Goodbye")
        expected_calls = [
            call.info("Hello Goodbye"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - tellList
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellList(self, mock_logging):
        log = TestLogger()

        log.tellList(["line1", "line2", "line3"], "line dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN line dump  =========="),
            call.info(""),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(""),
            call.info("==========  END line dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellList_no_title(self, mock_logging):
        log = TestLogger()

        log.tellList(["line1", "line2", "line3"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - tellMode
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellMode(self, mock_logging):
        """
        Test with no parameters
        """
        log = TestLogger()

        log.tellMode(TestLogger.Mode.PROD)
        log.tellMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellMode(TestLogger.Mode.PROD)
        log.tellMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellMode_object_None(self, mock_logging):
        """
        Test with None parameter
        """
        log = TestLogger()

        log.tellMode(TestLogger.Mode.PROD, None)
        log.tellMode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellMode(TestLogger.Mode.PROD, None)
        log.tellMode(TestLogger.Mode.TEST, None)
        expected_calls = [
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellMode_object_True(self, mock_logging):
        """
        Test with boolean parameter
        """
        log = TestLogger()

        log.tellMode(TestLogger.Mode.PROD, True)
        log.tellMode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("True"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellMode(TestLogger.Mode.PROD, True)
        log.tellMode(TestLogger.Mode.TEST, False)
        expected_calls = [
            call.info("False"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellMode_literal(self, mock_logging):
        """
        Test with single parameter
        """
        log = TestLogger()

        log.tellMode(TestLogger.Mode.PROD, "Hello {}")
        log.tellMode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Hello {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellMode(TestLogger.Mode.PROD, "Hello {}")
        log.tellMode(TestLogger.Mode.TEST, "Goodbye {}")
        expected_calls = [
            call.info("Goodbye {}"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellMode_format(self, mock_logging):
        """
        Test with format and value parameter
        """
        log = TestLogger()

        log.tellMode(TestLogger.Mode.PROD, "Hello {}", "there")
        log.tellMode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Hello there"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellMode(TestLogger.Mode.PROD, "Hello {}", "there")
        log.tellMode(TestLogger.Mode.TEST, "Goodbye {}", "y'all")
        expected_calls = [
            call.info("Goodbye y'all"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - tellModeList
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellModeList(self, mock_logging):
        log = TestLogger()

        log.tellModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        log.tellModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN prod dump  =========="),
            call.info(""),
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
            call.info(""),
            call.info("==========  END prod dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"], "prod dump")
        log.tellModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"], "test dump")
        expected_calls = [
            call.info(""),
            call.info("==========  BEGIN test dump  =========="),
            call.info(""),
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
            call.info(""),
            call.info("==========  END test dump  =========="),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_tellModeList_no_title(self, mock_logging):
        log = TestLogger()

        log.tellModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        log.tellModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("line1"),
            call.info("line2"),
            call.info("line3"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.setMode(TestLogger.Mode.TEST)
        expected_calls = [
            call.info("The logging mode is now TEST"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.tellModeList(TestLogger.Mode.PROD, ["line1", "line2", "line3"])
        log.tellModeList(TestLogger.Mode.TEST, ["lineA", "lineB", "lineC"])
        expected_calls = [
            call.info("lineA"),
            call.info("lineB"),
            call.info("lineC"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - warn
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warn__literal_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar", log.warn("foobar"))
        expected_calls = [
            call.warning("-WARN- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warn__format_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar foobar2", log.warn("foobar {}", "foobar2"))
        expected_calls = [
            call.warning("-WARN- : foobar foobar2"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warn__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        # Discard calls so that we don't have to verify them.
        mock_logging.mock_calls = []

        self.assertEqual("foobar", log.warn("foobar"))
        expected_calls = [
            call.warning("-WARN- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         1 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Warnings  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         1 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Warnings  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - warnException
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warnException(self, mock_logging):

        log = TestLogger()

        e = TypeError("foobar")
        log.warnException(e)
        expected_calls = [
            call.exception(e),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - warnOnce
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warnOnce__literal_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar", log.warnOnce("foobar"))
        self.assertEqual("foobar", log.warnOnce("foobar"))
        expected_calls = [
            call.warning("-WARN- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warnOnce__format_WithoutFeature(self, mock_logging):
        log = TestLogger()

        self.assertEqual("foobar foobar2", log.warnOnce("foobar {}", "foobar2"))
        self.assertEqual("foobar foobar2", log.warnOnce("foobar {}", "foobar2"))
        expected_calls = [
            call.warning("-WARN- : foobar foobar2"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_warnOnce__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        # Discard calls so that we don't have to verify them.
        mock_logging.mock_calls = []

        self.assertEqual("foobar", log.warnOnce("foobar"))
        self.assertEqual("foobar", log.warnOnce("foobar"))
        expected_calls = [
            call.warning("-WARN- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         2 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Warnings  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         2 : Total warnings"),
            call.info("         0 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Warnings  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    #####################################################################################################
    # METHOD - workaround
    #####################################################################################################

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_workaround__literal_WithoutFeature(self, mock_logging):
        log = TestLogger()

        log.workaround("foobar")
        log.workaround("foobar")
        expected_calls = [
            call.warning("-WORK- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_workaround__format_WithoutFeature(self, mock_logging):
        log = TestLogger()

        log.workaround("foobar {}", "foobar2")
        log.workaround("foobar {}", "foobar2")
        expected_calls = [
            call.warning("-WORK- : foobar foobar2"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

    @mock.patch('kojak.core.TestLogger.time')
    @mock.patch('kojak.core.TestLogger.logging')
    def test_method_workaround__literal_WithFeature(self, mock_logging, mock_time):
        mock_time.time.return_value = 0
        log = TestLogger()

        log.beginFeature("Feature")
        # Discard calls so that we don't have to verify them.
        mock_logging.mock_calls = []

        log.workaround("foobar")
        log.workaround("foobar")
        expected_calls = [
            call.warning("-WORK- : foobar"),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

        log.endFeature()
        expected_calls = [
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info("==========  BEGIN FEATURE SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         2 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Workarounds  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END FEATURE SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("==========  BEGIN RUN SUMMARY  =========="),
            call.info(""),
            call.info("RESULT: PASS"),
            call.info(""),
            call.info("         0 : Total tests"),
            call.info("         0 : Total failures"),
            call.info("         0 : Total warnings"),
            call.info("         2 : Total workarounds"),
            call.info(""),
            call.info("Elapsed time: 0 seconds"),
            call.info(""),
            call.info("-----  Unique Workarounds  -----"),
            call.info(""),
            call.info("foobar"),
            call.info(""),
            call.info("==========  END RUN SUMMARY  =========="),
            call.info(""),
            call.info(""),
            call.info("####################################################################################################"),
            call.info("END FEATURE Feature"),
            call.info("####################################################################################################"),
            call.info(""),
            call.info(""),
        ]
        self.assertEqual(mock_logging.mock_calls, expected_calls)
        mock_logging.mock_calls = []

if __name__ == '__main__':
    unittest.main()
