"""
Created on November 18, 2017

@author: John Jackson
"""

import unittest

from kojak.core.utilities import luhn_algorithm as la


###############################################################################
# TEST MODULE
###############################################################################

class Test(unittest.TestCase):

    # =========================================================================
    # METHOD - add_checksum
    # =========================================================================

    def test_add_checksum(self):
        self.assertEqual('0', la.add_checksum(None))
        self.assertEqual('0', la.add_checksum(''))

        self.assertEqual('00', la.add_checksum('0'))
        self.assertEqual('18', la.add_checksum('1'))
        self.assertEqual('26', la.add_checksum('2'))
        self.assertEqual('34', la.add_checksum('3'))
        self.assertEqual('42', la.add_checksum('4'))
        self.assertEqual('59', la.add_checksum('5'))
        self.assertEqual('67', la.add_checksum('6'))
        self.assertEqual('75', la.add_checksum('7'))
        self.assertEqual('83', la.add_checksum('8'))
        self.assertEqual('91', la.add_checksum('9'))

        self.assertEqual('018', la.add_checksum('01'))
        self.assertEqual('117', la.add_checksum('11'))
        self.assertEqual('216', la.add_checksum('21'))
        self.assertEqual('315', la.add_checksum('31'))
        self.assertEqual('414', la.add_checksum('41'))
        self.assertEqual('513', la.add_checksum('51'))
        self.assertEqual('612', la.add_checksum('61'))
        self.assertEqual('711', la.add_checksum('71'))
        self.assertEqual('810', la.add_checksum('81'))
        self.assertEqual('919', la.add_checksum('91'))

        self.assertEqual('6006493865249902504', la.add_checksum('600649386524990250'))
        self.assertEqual('6006493865249902512', la.add_checksum('600649386524990251'))
        self.assertEqual('6006493865249902520', la.add_checksum('600649386524990252'))
        self.assertEqual('6006493865249902538', la.add_checksum('600649386524990253'))
        self.assertEqual('6006493865249902546', la.add_checksum('600649386524990254'))
        self.assertEqual('6006493865249902553', la.add_checksum('600649386524990255'))
        self.assertEqual('6006493865249902561', la.add_checksum('600649386524990256'))
        self.assertEqual('6006493865249902579', la.add_checksum('600649386524990257'))
        self.assertEqual('6006493865249902587', la.add_checksum('600649386524990258'))
        self.assertEqual('6006493865249902595', la.add_checksum('600649386524990259'))

    def test_add_checksum__value_error(self):
        self.assertRaises(ValueError, la.add_checksum, 'hello')

    # =========================================================================
    # METHOD - add_prefix
    # =========================================================================

    def test_add_prefix(self):
        self.assertEqual('', la.add_prefix(None, None))
        self.assertEqual('12345', la.add_prefix(None, '12345'))
        self.assertEqual('12345', la.add_prefix('', '12345'))
        self.assertEqual('7612345', la.add_prefix('7', '12345'))
        self.assertEqual('77412345', la.add_prefix('77', '12345'))
        self.assertEqual('75123456', la.add_prefix('7', '123456'))
        self.assertEqual('778123456', la.add_prefix('77', '123456'))

        # Just returns the number; no exception is expected.
        self.assertEqual('hello', la.add_prefix(None, 'hello'))

    def test_add_prefix__value_error(self):
        self.assertRaises(ValueError, la.add_prefix, 'hello')

    # =========================================================================
    # METHOD - get_check_digit
    # =========================================================================

    def test_get_check_digit(self):
        self.assertEqual(0, la.get_check_digit(None))
        self.assertEqual(0, la.get_check_digit(''))

        self.assertEqual(0, la.get_check_digit('0'))
        self.assertEqual(8, la.get_check_digit('1'))
        self.assertEqual(6, la.get_check_digit('2'))
        self.assertEqual(4, la.get_check_digit('3'))
        self.assertEqual(2, la.get_check_digit('4'))
        self.assertEqual(9, la.get_check_digit('5'))
        self.assertEqual(7, la.get_check_digit('6'))
        self.assertEqual(5, la.get_check_digit('7'))
        self.assertEqual(3, la.get_check_digit('8'))
        self.assertEqual(1, la.get_check_digit('9'))

        self.assertEqual(8, la.get_check_digit('01'))
        self.assertEqual(7, la.get_check_digit('11'))
        self.assertEqual(6, la.get_check_digit('21'))
        self.assertEqual(5, la.get_check_digit('31'))
        self.assertEqual(4, la.get_check_digit('41'))
        self.assertEqual(3, la.get_check_digit('51'))
        self.assertEqual(2, la.get_check_digit('61'))
        self.assertEqual(1, la.get_check_digit('71'))
        self.assertEqual(0, la.get_check_digit('81'))
        self.assertEqual(9, la.get_check_digit('91'))

    def test_get_check_digit__value_error(self):
        self.assertRaises(ValueError, la.get_check_digit, 'hello')

    # =========================================================================
    # METHOD - get_checksum
    # =========================================================================

    def test_get_checksum(self):
        self.assertEqual(0, la.get_checksum(None))
        self.assertEqual(0, la.get_checksum(''))

        self.assertEqual(0, la.get_checksum('0'))
        self.assertEqual(2, la.get_checksum('1'))
        self.assertEqual(4, la.get_checksum('2'))
        self.assertEqual(6, la.get_checksum('3'))
        self.assertEqual(8, la.get_checksum('4'))
        self.assertEqual(1, la.get_checksum('5'))
        self.assertEqual(3, la.get_checksum('6'))
        self.assertEqual(5, la.get_checksum('7'))
        self.assertEqual(7, la.get_checksum('8'))
        self.assertEqual(9, la.get_checksum('9'))

        self.assertEqual(2, la.get_checksum('01'))
        self.assertEqual(3, la.get_checksum('11'))
        self.assertEqual(4, la.get_checksum('21'))
        self.assertEqual(5, la.get_checksum('31'))
        self.assertEqual(6, la.get_checksum('41'))
        self.assertEqual(7, la.get_checksum('51'))
        self.assertEqual(8, la.get_checksum('61'))
        self.assertEqual(9, la.get_checksum('71'))
        self.assertEqual(0, la.get_checksum('81'))
        self.assertEqual(1, la.get_checksum('91'))

    def test_get_checksum__value_error(self):
        self.assertRaises(ValueError, la.get_checksum, 'hello')

    # =========================================================================
    # METHOD - set_checksum
    # =========================================================================

    def test_set_checksum(self):
        self.assertEqual('0', la.set_checksum(None))
        self.assertEqual('0', la.set_checksum(''))

        self.assertEqual('0', la.set_checksum('0'))
        self.assertEqual('0', la.set_checksum('1'))
        self.assertEqual('0', la.set_checksum('2'))
        self.assertEqual('0', la.set_checksum('3'))
        self.assertEqual('0', la.set_checksum('4'))
        self.assertEqual('0', la.set_checksum('5'))
        self.assertEqual('0', la.set_checksum('6'))
        self.assertEqual('0', la.set_checksum('7'))
        self.assertEqual('0', la.set_checksum('8'))
        self.assertEqual('0', la.set_checksum('9'))

        self.assertEqual('00', la.set_checksum('01'))
        self.assertEqual('18', la.set_checksum('11'))
        self.assertEqual('26', la.set_checksum('21'))
        self.assertEqual('34', la.set_checksum('31'))
        self.assertEqual('42', la.set_checksum('41'))
        self.assertEqual('59', la.set_checksum('51'))
        self.assertEqual('67', la.set_checksum('61'))
        self.assertEqual('75', la.set_checksum('71'))
        self.assertEqual('83', la.set_checksum('81'))
        self.assertEqual('91', la.set_checksum('91'))

    def test_set_checksum__value_error(self):
        self.assertRaises(ValueError, la.set_checksum, 'hello')

    # =========================================================================
    # METHOD - verify_checksum
    # =========================================================================

    def test_verify_checksum(self):

        self.assertTrue(la.verify_checksum(None))
        self.assertTrue(la.verify_checksum(''))

        self.assertTrue(la.verify_checksum('00'))
        self.assertTrue(la.verify_checksum('18'))
        self.assertTrue(la.verify_checksum('26'))
        self.assertTrue(la.verify_checksum('34'))
        self.assertTrue(la.verify_checksum('42'))
        self.assertTrue(la.verify_checksum('59'))
        self.assertTrue(la.verify_checksum('67'))
        self.assertTrue(la.verify_checksum('75'))
        self.assertTrue(la.verify_checksum('83'))
        self.assertTrue(la.verify_checksum('91'))

        self.assertTrue(la.verify_checksum('018'))
        self.assertTrue(la.verify_checksum('117'))
        self.assertTrue(la.verify_checksum('216'))
        self.assertTrue(la.verify_checksum('315'))
        self.assertTrue(la.verify_checksum('414'))
        self.assertTrue(la.verify_checksum('513'))
        self.assertTrue(la.verify_checksum('612'))
        self.assertTrue(la.verify_checksum('711'))
        self.assertTrue(la.verify_checksum('810'))
        self.assertTrue(la.verify_checksum('919'))

        self.assertFalse(la.verify_checksum('10'))
        self.assertFalse(la.verify_checksum('118'))

    def test_verify_checksum__value_error(self):
        self.assertRaises(ValueError, la.verify_checksum, 'hello')
