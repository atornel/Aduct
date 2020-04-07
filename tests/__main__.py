import unittest

from tests.TestBin import TestBin
from tests.TestElement import TestElement
from tests.TestNotebook import TestNotebook
from tests.TestPaned import TestPaned

if __name__ == "__main__":

    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestBin))
    suite.addTest(unittest.makeSuite(TestElement))
    suite.addTest(unittest.makeSuite(TestNotebook))
    suite.addTest(unittest.makeSuite(TestPaned))
    runner = unittest.TextTestRunner()
    runner.run(suite)
