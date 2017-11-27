"""
Created on November 5, 2017

@author: John Jackson
"""


def verify_mock_calls(test_case, actual, expected, description=None):
    """
    Used by various unit tests to verify a list of mock calls.
    The method makes it easier to see what is wrong if the verification fails
    by logging both lists and indicating where the first discrepancy appears.

    :param unittest.TestCase test_case: The unittest TestCase object calling
        this method.
    :param list[unittest.mock.call] actual: A list from mock.mock_calls.
    :param list[unittest.mock.call,str] expected: A list of mock call
        objects to compare against the actual list.  Optionally, an entry
        may be a string, in which case it and it's companion entry
        in **actual** are ignored.
    :param str description: A short description of the test case to log in case
        the verification fails.
    :rtype: None
    :raises AssertionError: The verification fails.
    """

    i = 0
    try:
        while i < len(expected) and i < len(actual):
            if not isinstance(expected[i], str):
                test_case.assertEqual(expected[i], actual[i], description)
            i += 1
        test_case.assertEqual(len(expected), len(actual), description)
        actual.clear()
    except AssertionError:
        print("Mis-match at index %d" % i)
        print(str(expected[i]) + "," if i < len(expected) else '-----')
        print(str(actual[i]) + "," if i < len(actual) else '-----')
        print("")
        print("Expected call list:")
        for e in expected:
            print(str(e) + ",")
        print("")
        print("Actual call list:")
        for a in actual:
            print(str(a) + ",")
        raise


def verify_lists(test_case, actual, expected):
    """
    Used by various unit tests to verify a list of objects.
    The method makes it easier to see what is wrong if the verification fails
    by logging both lists and indicating where the first discrepancy appears.

    :param unittest.TestCase test_case: The unittest TestCase object calling
        this method.
    :param list actual: The list of objects to verify.
    :param list expected: A list of objects to compare against
        the actual list.
    :rtype: None
    :raises AssertionError: The verification fails.
    """

    i = 0
    try:
        while i < len(expected) and i < len(actual):
            test_case.assertEqual(expected[i], actual[i])
            i += 1
        test_case.assertEqual(len(expected), len(actual))
        actual.clear()
    except AssertionError:
        print("Mis-match at index %d" % i)
        print(repr(expected[i]) + "," if i < len(expected) else '-----')
        print(repr(actual[i]) + "," if i < len(actual) else '-----')
        print("")
        print("Expected list:")
        for e in expected:
            print(repr(e) + ",")
        print("")
        print("Actual list:")
        for a in actual:
            print(repr(a) + ",")
        raise
