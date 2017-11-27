"""
Created on January 27, 2017

@author: John Jackson
"""

import logging
import time
from enum import IntEnum
from typing import List

from kojak.core.utilities import string_library as sl


class TestLogger:
    """
    This class provides a variety of methods for logging test results.
    """

    ###########################################################################
    # CONSTANTS
    ###########################################################################

    # Specifies the minimum length banner for print_banner to generate.
    _MIN_BANNER_LENGTH: int = 100

    _BANNER_SNIPPET_HASH: str = "##########"
    _BANNER_SNIPPET_EQUAL: str = "=========="
    _BANNER_SNIPPET_PLUS: str = "++++++++++"
    _BANNER_SNIPPET_DASH: str = "-----"

    _FEATURE_TAG: str = " Feature: "
    _SCENARIO_TAG: str = " Scenario: "
    _SECTION_TAG: str = " Section: "
    _GIVEN_TAG: str = " Given: "
    _WHEN_TAG: str = " When: "
    _THEN_TAG: str = " Then: "

    ###########################################################################
    # ENUM : Mode
    ###########################################################################

    class Mode(IntEnum):

        # Specifies that you want to log the message only when the system
        # is in TEST mode.
        TEST = 1

        # Specifies that you want to log the message only when the system
        # is in PRODUCTION mode.  These messages usually carry sensitive
        # information, such as passwords, etc.
        PROD = 2

    # #########################################################################
    # CLASS - ReportStats
    # #########################################################################

    class ReportStats:
        """
        This class collects run-time test statistics
        """

        #######################################################################
        # METHODS
        #######################################################################

        # =====================================================================
        # CONSTRUCTOR
        # =====================================================================

        def __init__(self):

            # Tracks the number of failures reported.
            self._failure_count: int = 0

            # Tracks the number of failures reported while discarding
            # duplicate failure messages.
            self._failures: set = set()

            # Holds the start-time of the test run.
            self._start_time: int = int(round(time.time() * 1000))

            # Tracks the number of tests executed.
            self._test_count: int = 0

            # Tracks the number of warnings reported.
            self._warning_count: int = 0

            # Tracks the number of warnings reported while discarding
            # duplicate warning messages.
            self._warnings: set = set()

            # Tracks the number of workarounds reported.
            self._workaround_count: int = 0

            # Tracks the number of workarounds reported while discarding
            # duplicate workaround messages.
            self._workarounds: set = set()

        # =====================================================================
        # add_failure
        # =====================================================================

        def add_failure(self, description: str) -> bool:
            """
            Tracks a failure, incrementing both the failure count and the
            test count.

            :param description: A description of the failure.
            :return: Returns true if this is the first time that the failure
                has been logged.
            """

            self._test_count += 1
            self._failure_count += 1
            first_occurrence: bool = description in self._failures
            self._failures.add(description)
            return first_occurrence

        # =====================================================================
        # add_test
        # =====================================================================

        def add_test(self) -> None:
            """
            Tracks a test execution and increments the test count.
            """

            self._test_count += 1

        # =====================================================================
        # add_warning
        # =====================================================================

        def add_warning(self, description: str) -> bool:
            """
            Tracks a warning and increments the warning count.

            :param description: A description of the warning.
            :return: Returns true if this is the first time that the warning
                has been logged.
            """

            self._warning_count += 1
            first_occurrence: bool = description in self._warnings
            self._warnings.add(description)
            return first_occurrence

        # =====================================================================
        # add_workaround
        # =====================================================================

        def add_workaround(self, description: str) -> bool:
            """
            Tracks a workaround and increments the workaround count.

            :param description: A description of the workaround.
            :return: Returns true if this is the first time that the workaround
                has been logged.
            """

            self._workaround_count += 1
            first_occurrence: bool = description in self._workarounds
            self._workarounds.add(description)
            return first_occurrence

        # =====================================================================
        # log_results
        # =====================================================================

        def log_results(self, logger: 'TestLogger') -> None:
            """
            Logs the accumulated statistics.
            """

            # Indicate the gross PASS/FAIL status of the results.
            if self._failure_count == 0:
                logger.info("RESULT: PASS")
            else:
                logger.info("RESULT: FAIL")
            logger.info("")

            # Log the counters
            logger.info("{:10d} : Total tests".format(self._test_count))
            logger.info("{:10d} : Total failures".format(self._failure_count))
            logger.info("{:10d} : Total warnings".format(self._warning_count))
            logger.info("{:10d} : Total workarounds".format(
                self._workaround_count))
            logger.info("")

            # Log the elapsed time
            stop_time: int = int(round(time.time() * 1000))
            elapsed_time = stop_time - self._start_time
            logger.info(
                "Elapsed time: {}".format(
                    sl.to_elapsed_time_verbose(elapsed_time)))

            # Itemize the unique failure messages
            if len(self._failures) > 0:
                logger.print_header_dash("Unique Failures")
                for failure in self._failures:
                    logger.info(failure)

            # Itemize the unique warning messages
            if len(self._warnings) > 0:
                logger.print_header_dash("Unique Warnings")
                for warning in self._warnings:
                    logger.info(warning)

            # Itemize the unique workaround messages
            if len(self._workarounds) > 0:
                logger.print_header_dash("Unique Workarounds")
                for workaround in self._workarounds:
                    logger.info(workaround)

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self):

        # Holds the statistics being collected for the current feature.
        # Is set to None if no feature is active.
        self._feature_stats: 'TestLogger.ReportStats' = None

        # Holds the last header set by print_header_begin.
        # Is set to "" if no feature is active.
        self._last_begin_header: str = ""

        # Holds the last header set by begin_feature.
        # Is set to "" if no feature is active.
        self._last_feature_header: str = ""

        # Holds the last header set by begin_given.
        self._last_given_header: str = ""

        # Holds the last header set by begin_scenario.
        self._last_scenario_header: str = ""

        # Holds the last header set by begin_section.
        self._last_section_header: str = ""

        # Holds the last header set by begin_then.
        self._last_then_header: str = ""

        # Holds the last header set by begin_when.
        self._last_when_header: str = ""

        # Holds the mode for logging sensitive information.
        self._mode: TestLogger.Mode = TestLogger.Mode.PROD

        # Holds the statistics being collected for the entire test run.
        self._run_stats: TestLogger.ReportStats = TestLogger.ReportStats()

        # When set true, all calls to info are ignored.
        self._suppress_info_output: bool = False

    # =========================================================================
    # begin_feature
    # =========================================================================

    def begin_feature(self, feature_name: str) -> None:
        """
        Makes a notation in the log file that the testing of a new feature
        has begun.  Note: This method automatically calls **end_feature**
        if you haven't already called it to terminate the previous feature.

        :param feature_name: The name of the feature.
        """

        # Terminate the previous feature if it is still active
        if self._feature_stats is not None:
            self.end_feature()

        # Store the feature name and clear all of the sub-headers
        self._last_feature_header = feature_name or "unknown"
        self._last_scenario_header = ""
        self._last_section_header = ""
        self._last_given_header = ""
        self._last_when_header = ""
        self._last_then_header = ""

        # Begin a new statistics accumulator for this feature
        self._feature_stats = TestLogger.ReportStats()

        # Print the banner announcing the new header
        self.print_banner(
            "BEGIN FEATURE " + self._last_feature_header, 2, 2, 2, 2)

    # =========================================================================
    # begin_given
    # =========================================================================

    def begin_given(self, given_statement: str) -> None:
        """
        Makes a notation in the log file that a 'Given' statement
        is being executed.

        :param given_statement: The text of the statement.
        """

        # Store the 'Given' statement and clear all the lower headers.
        self._last_given_header = given_statement or ""
        self._last_when_header = ""
        self._last_then_header = ""

        # Print the banner announcing the new 'Given' statement
        self.print_banner(self._FEATURE_TAG + self._last_feature_header, 2, 1)
        self.print_banner(self._SCENARIO_TAG + self._last_scenario_header)
        self.print_banner(self._SECTION_TAG + self._last_section_header)
        self.print_banner(
            self._GIVEN_TAG + self._last_given_header, 0, 0, 1, 2)

    # =========================================================================
    # begin_scenario
    # =========================================================================

    def begin_scenario(self, scenario_name: str) -> None:
        """
        Makes a notation in the log file that the testing of a new scenario
        within the current feature has begun.

        :param scenario_name: The name of the scenario.
        """

        # Store the Scenario name and clear all the lower headers.
        self._last_scenario_header = scenario_name or ""
        self._last_section_header = ""
        self._last_given_header = ""
        self._last_when_header = ""
        self._last_then_header = ""

        # Print the banner announcing the new scenario
        self.print_banner(
            self._FEATURE_TAG + self._last_feature_header, 2, 1)
        self.print_banner(
            self._SCENARIO_TAG + self._last_scenario_header, 0, 0, 1, 2)

    # =========================================================================
    # begin_section
    # =========================================================================

    def begin_section(self, section_name: str) -> None:
        """
        Makes a notation in the log file that the testing of a new section
        within the current scenario has begun.

        :param section_name: The text of the statement.
        """

        # Store the section name and clear all the lower headers
        self._last_section_header = section_name or ""
        self._last_given_header = ""
        self._last_when_header = ""
        self._last_then_header = ""

        # We don't print a banner since no actual action will be taken

    # =========================================================================
    # begin_then
    # =========================================================================

    def begin_then(self, then_statement: str) -> None:
        """
        Makes a notation in the log file that a 'Then' statement
        is being executed.

        :param then_statement: The text of the statement.
        """

        # Store the 'Then' statement; there are no lower headers to clear
        self._last_then_header = then_statement or ""

        # Print the banner announcing the 'Then' statement
        self.print_banner(self._FEATURE_TAG + self._last_feature_header, 2, 1)
        self.print_banner(self._SCENARIO_TAG + self._last_scenario_header)
        self.print_banner(self._SECTION_TAG + self._last_section_header)
        self.print_banner(self._GIVEN_TAG + self._last_given_header)
        self.print_banner(self._WHEN_TAG + self._last_when_header)
        self.print_banner(self._THEN_TAG + self._last_then_header, 0, 0, 1, 2)

    # =========================================================================
    # begin_when
    # =========================================================================

    def begin_when(self, when_statement: str) -> None:
        """
        Makes a notation in the log file that a 'When' statement
        is being executed.

        :param when_statement: The text of the statement.
        """

        # Store the 'When' statement and clear all the lower headers
        self._last_when_header = when_statement or ""
        self._last_then_header = ""

        # Print the banner announcing the 'When' statement
        self.print_banner(self._FEATURE_TAG + self._last_feature_header, 2, 1)
        self.print_banner(self._SCENARIO_TAG + self._last_scenario_header)
        self.print_banner(self._SECTION_TAG + self._last_section_header)
        self.print_banner(self._GIVEN_TAG + self._last_given_header)
        self.print_banner(self._WHEN_TAG + self._last_when_header, 0, 0, 1, 2)

    # =========================================================================
    # end_feature
    # =========================================================================

    def end_feature(self) -> None:
        """
        Prints a banner to mark the end of the feature and prints out
        the cumulative statistics since begin_feature was last called.
        """

        # Disable info output suppression in case the current feature
        # didn't already do so.
        self.set_suppress_info_output(False)

        # Print out the feature statistics if a feature is active
        if self._feature_stats is not None:
            # Announce the end of the feature and announce the feature's
            # statistics
            self.print_banner(
                "END FEATURE " + self._last_feature_header, 2, 1, 1, 0)
            self.print_header_begin("FEATURE SUMMARY")
            self._feature_stats.log_results(self)
            self.print_header_end()

        # As a convenience to the caller (hopefully), log the running
        # statistics
        self.print_header_begin("RUN SUMMARY")
        self._run_stats.log_results(self)
        self.print_header_end()

        # Close out the statistics dump
        if self._feature_stats is not None:
            # Announce the end of the feature and announce the feature's
            # statistics
            self.print_banner(
                "END FEATURE " + self._last_feature_header, 1, 1, 1, 2)
            # Indicate that no feature is active
            self._feature_stats = None

    # =========================================================================
    # fail_test
    # =========================================================================

    def fail_test(self, reason: str, *args) -> str:
        """
        Increments the test and fail counters and logs the given failure
        reason.

        :param reason: The reason for the failure.
        :param args: Arguments to apply to **reason**; omit to treat **reason**
            as a literal.
        :return: the given failure reason formatted via ``str.format()``
            if you supplied **args**.
        """

        # If there are no arguments then treat the reason string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            reason = reason.format(*args)

        # Update the statistics for the whole run as well as for the current
        # feature.
        self._run_stats.add_failure(reason)
        logging.error("-FAIL- : " + reason)

        if self._feature_stats is not None:
            self._feature_stats.add_failure(reason)

        return reason

    # =========================================================================
    # get_mode
    # =========================================================================

    def get_mode(self) -> Mode:
        """
        Returns the current mode for logging sensitive information.

        :return: the current mode for logging sensitive information.
        """

        return self._mode

    # =========================================================================
    # info...
    # =========================================================================

    def _info(self, message: str) -> str:
        """
        Sends the given message straight to the ``info`` method of the system
        Logger.

        :param message: The message to log.
        :return: the given message.
        """

        if not self._suppress_info_output:
            logging.info(message)

        return message

    def info(self, message: object = None, *args) -> str:
        """
        Prints a message to the log file if ``set_suppress_info_output(True)``
        has not been called previously.

        :param message: The message to log; omit to log a blank line.
        :param args: Arguments to apply to **message**;
            omit to treat **message** as a literal.
        :return: the given message formatted via ``str.format()``
            if you supplied **args**.
        """

        # Print a blank line if no parameters are given
        if message is None:
            message = ""

        else:
            # Make sure the message is a string.
            message = str(message)
            # If there are no arguments then treat the message string
            # as a literal; otherwise, treat it as a format string.
            if len(args) > 0:
                message = message.format(*args)

        # Log the message.
        return self._info(message)

    def info_list(self, lines: List[str], title: str = "") -> None:
        """
        Prints a list of messages to the log file if
        ``set_suppress_info_output(True)`` has not been called previously.

        :param lines: The messages to log.
        :param title: A title line describing the information being logged.
        """

        if title:
            self.print_header_begin(title)

        for line in lines:
            self._info(line)

        if title:
            self.print_header_end()

    def info_mode(self, mode: Mode, message: object = None, *args) -> str:
        """
        Prints a message to the log file if the given mode matches the current
        logger mode (see ``set_mode``) and ``set_suppress_info_output(True)``
        has not been called previously; otherwise, discards the message
        and returns the empty string.

        :param mode: The mode to log the message.
        :param message: The message to log; omit to log a blank line.
        :param args: Arguments to apply to **message**;
            omit to treat **message** as a literal.
        :return: the given message formatted via ``str.format()``
            if you supplied **args**.
        """
        return self.info(message, *args) if self._mode == mode else ""

    def info_mode_list(
            self, mode: Mode, lines: List[str], title: str = "") -> None:
        """
        Prints a list of messages to the log file if the given mode matches
        the current logger mode (see ``set_mode``) and
        ``set_suppress_info_output(True)`` has not been called previously.

        :param mode: The mode to log the message.
        :param lines: The messages to log.
        :param title: A title line describing the information being logged.
        """

        if self._mode == mode:
            self.info_list(lines, title)

    # =========================================================================
    # pass_test
    # =========================================================================

    def pass_test(self, reason: str, *args) -> str:
        """
        Increments the test count and the pass count, and logs the given
        success reason.

        :param reason: The reason for the success.
        :param args: Arguments to apply to **reason**;
            omit to treat **reason** as a literal.
        :return: the given success reason formatted via ``str.format()``
            if you supplied **args**.
        """

        # If there are no arguments then treat the reason string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            reason = reason.format(*args)

        # Update the statistics for the whole run as well as for the current
        # feature.
        self._run_stats.add_test()
        if self._feature_stats is not None:
            self._feature_stats.add_test()

        self._info(" PASS  : " + reason)

        return reason

    # =========================================================================
    # print_banner
    # =========================================================================

    def print_banner(
            self, message: str, blanks_before: int = 0,
            banners_before: int = 0, banners_after: int = 0,
            blanks_after: int = 0,
            banner_snippet: str = _BANNER_SNIPPET_HASH) -> None:
        """
        Prints out a banner to mark the start of a significant section
        of your test.

        :param message: The message to print.
        :param blanks_before: The number of blank lines to print before
            printing the banner lines.
        :param banners_before: The number of banner lines to print before
            printing the message.
        :param banners_after: The number of banner lines to print after
            printing the message.
        :param blanks_after: The number of blank lines to print after
            printing the banner lines.
        :param banner_snippet: A string to use to make the banner lines.
        """

        # Build the banner.
        banner = ""
        if banner_snippet:
            banner_length = max(self._MIN_BANNER_LENGTH, len(message))
            current_length: int = 0
            snippets: List[str] = []
            while current_length < banner_length:
                current_length += len(banner_snippet)
                snippets.append(banner_snippet)
            banner = ''.join(snippets)[0:banner_length]
        else:
            banners_before = 0
            banners_after = 0

        for _ in range(blanks_before):
            self._info("")

        for _ in range(banners_before):
            self._info(banner)

        self._info(message)

        for _ in range(banners_after):
            self._info(banner)

        for _ in range(blanks_after):
            self._info("")

    # =========================================================================
    # printHeader ...
    # =========================================================================

    def print_header_begin(self, title: str, *args) -> None:
        """
        Prints a minor header using the character "-" for the banner
        and prepends BEGIN to the title.
        You should later call ``print_header_end`` to close the header.

        :param title: The title to print with the header.
        :param args: Arguments to apply to **title**;
            omit to treat **title** as a literal.
        """

        # Close the previous header if it has not already been closed.
        if self._last_begin_header:
            self.print_header_end()

        title = "-unspecified-" if not title else title \
            if len(args) == 0 else title.format(*args)
        self._last_begin_header = title

        self._info("")
        self._info(self._BANNER_SNIPPET_EQUAL
                   + "  BEGIN "
                   + self._last_begin_header
                   + "  "
                   + self._BANNER_SNIPPET_EQUAL)
        self._info("")

    def print_header_dash(self, title: str, *args) -> None:
        """
        Prints a minor header using the character "-" for the banner.

        :param title: The title to print with the header.
        :param args: Arguments to apply to **title**;
            omit to treat **title** as a literal.
        """

        # If there are no arguments then treat the message string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            title = title.format(*args)

        self._info("")
        self._info(self._BANNER_SNIPPET_DASH
                   + "  "
                   + title
                   + "  "
                   + self._BANNER_SNIPPET_DASH)
        self._info("")

    def print_header_end(self) -> None:
        """
        Prints a minor header using the character "-" for the banner
        and prepends END to the title.
        Uses the title last submitted to ``print_header_begin``.
        """

        if self._last_begin_header:
            self._info("")
            self._info(self._BANNER_SNIPPET_EQUAL
                       + "  END "
                       + self._last_begin_header
                       + "  "
                       + self._BANNER_SNIPPET_EQUAL)
            self._info("")
            self._last_begin_header = ""

    def print_header_equal(self, title: str, *args) -> None:
        """
        Prints a minor header using the character "=" for the banner.

        :param title: The title to print with the header.
        :param args: Arguments to apply to **title**;
            omit to treat **title** as a literal.
        """

        # If there are no arguments then treat the message string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            title = title.format(*args)

        self.print_banner(title, 1, 1, 1, 0, self._BANNER_SNIPPET_EQUAL)

    def print_header_plus(self, title: str, *args) -> None:
        """
        Prints a minor header using the character "+" for the banner.

        :param title: The title to print with the header.
        :param args: Arguments to apply to **title**;
            omit to treat **title** as a literal.
        """

        # If there are no arguments then treat the message string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            title = title.format(*args)

        self.print_banner(title, 1, 1, 1, 0, self._BANNER_SNIPPET_PLUS)

    # =========================================================================
    # set_mode
    # =========================================================================

    def set_mode(self, m: Mode = Mode.PROD) -> Mode:
        """
        Sets the mode for logging sensitive information.

        :param m: The new mode to use.
        :return: the current mode.
        """

        if m != self._mode:
            self._info("The logging mode is now {}".format(m.name))

        temp = self._mode
        self._mode = m
        return temp

    # =========================================================================
    # set_suppress_info_output
    # =========================================================================

    def set_suppress_info_output(self, value: bool) -> bool:
        """
        Enables/Disabled any output from the info method.

        :param value: Use True to disable the ``info`` method;
            use False to enable it.
        :return: the current mode.
        """

        temp = self._suppress_info_output
        if value != temp:
            # Since we know the we are changing the value of
            # 'suppressInfoOutput' then only one of the following
            # info statements will be output.
            self.info("Disabling info output")
            self._suppress_info_output = value
            self.info("Enabling info output")

        return temp

    # =========================================================================
    # tell
    # =========================================================================

    @staticmethod
    def tell(message: object = None, *args) -> str:
        """
        Prints a message to the log file.

        :param message: The message to log; omit to log a blank line.
        :param args: Arguments to apply to **message**;
            omit to treat **message** as a literal.
        :return: the given message formatted via ``str.format()``
            if you supplied **args**.
        """

        # Print a blank line if no parameters are given
        if message is None:
            message = ""

        else:
            # Make sure the message is a string.
            message = str(message)
            # If there are no arguments then treat the message string
            # as a literal; otherwise, treat it as a format string.
            if len(args) > 0:
                message = message.format(*args)

        # Log the message.
        logging.info(message)

        return message

    def tell_list(self, lines: List[str], title: str = "") -> None:
        """
        Prints a list of messages to the log file.

        :param title: A title line describing the information being logged.
        :param lines: The messages to log.
        """

        if title:
            self.print_header_begin(title)

        for line in lines:
            logging.info(line)

        if title:
            self.print_header_end()

    def tell_mode(self, mode: Mode, message: object = None, *args) -> str:
        """
        Prints a message to the log file if the given mode matches the current
        logger mode (see ``set_mode``); otherwise, discards the message
        and returns the empty string.

        :param mode: The mode to log the message.
        :param message: The message to log; omit to log a blank line.
        :param args: Arguments to apply to **message**;
            omit to treat **message** as a literal.
        :return: the given message formatted via ``str.format()``
            if you supplied **args**.
        """
        return self.tell(message, *args) if self._mode == mode else ""

    def tell_mode_list(
            self, mode: Mode, lines: List[str], title: str = "") -> None:
        """
        Prints a list of messages to the log file if the given mode matches
        the current logger mode (see ``set_mode``).

        :param mode: The mode to log the message.
        :param title: A title line describing the information being logged.
        :param lines: The messages to log.
        """

        if self._mode == mode:
            self.tell_list(lines, title)

    # =========================================================================
    # warn
    # =========================================================================

    def warn(self, reason: str, *args) -> str:
        """
        Increments the warning count, but not the test count, and logs
        the given warning reason.

        :param reason: The reason to log.
        :param args: Arguments to apply to **reason**;
            omit to treat **reason** as a literal.
        :return: the given reason formatted via ``str.format()``
            if you supplied **args**.
        """

        # If there are no arguments then treat the reason string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            reason = reason.format(*args)

        # Update the statistics for the whole run as well as for the
        # current feature.
        self._run_stats.add_warning(reason)
        logging.warning("-WARN- : " + reason)

        if self._feature_stats is not None:
            self._feature_stats.add_warning(reason)

        return reason

    # =========================================================================
    # warn_exception
    # =========================================================================

    @staticmethod
    def warn_exception(e: Exception) -> None:
        """
        Increments the warning count, but not the test count, and logs
        the given Exception as a warning.

        :param e: The Exception to log.
        """

        logging.exception(e)

    # =========================================================================
    # warn_once
    # =========================================================================

    def warn_once(self, reason: str, *args) -> str:
        """
        Increments the warning count, but not the test count, and logs
        the given warning reason if it has not already been logged once before.

        :param reason: The reason to log.
        :param args: Arguments to apply to **reason**;
            omit to treat **reason** as a literal.
        :return: the given reason formatted via ``str.format()``
            if you supplied **args**.
        """

        # If there are no arguments then treat the reason string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            reason = reason.format(*args)

        # Update the statistics for the whole run as well as for
        # the current feature.
        if self._run_stats.add_warning(reason):
            logging.warning("-WARN- : " + reason)

        if self._feature_stats is not None:
            self._feature_stats.add_warning(reason)

        return reason

    # =========================================================================
    # workaround
    # =========================================================================

    def workaround(self, reason: str, *args) -> None:
        """
        Increments the workaround count, but not the test count, and logs
        the given workaround reason. A workaround message reminds you that
        you have a 'workaround' in your test script to get past
        a bug with the system that you are testing.

        :param reason: The workaround reminder message.
        :param args: Arguments to apply to **reason**;
            omit to treat **reason** as a literal.
        """

        # If there are no arguments then treat the reason string as a literal;
        # otherwise, treat it as a format string.
        if len(args) > 0:
            reason = reason.format(*args)

        # Update the statistics for the whole run as well as for
        # the current feature.
        if self._run_stats.add_workaround(reason):
            logging.warning("-WORK- : " + reason)

        if self._feature_stats is not None:
            self._feature_stats.add_workaround(reason)
