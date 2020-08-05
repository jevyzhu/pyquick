from pyquick.main import arg_parser
import unittest

class test_tf_mini(unittest.TestCase):
    def test_1(self):
        with self.assertRaises(SystemExit):
            arg = arg_parser().parse_args(['--version'])
            assert arg.version == 'quick 0.0.1'
