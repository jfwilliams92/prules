import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pystrategy import Evaluation

class TestEvaluation(unittest.TestCase):
    
    def test_lt(self):
        ev = Evaluation("Money", 500, "lt")
        ev_test = {"Money": 400}
        self.assertTrue(ev.evaluate(ev_test), "Nope!")

        ev = Evaluation("Money", 500.0, "lt")
        ev_test = {"Money": 650.43}
        self.assertFalse(ev.evaluate(ev_test), "Nope")

        ev = Evaluation("OfferDate", "2020-01-23", "lt")
        ev_test = {"OfferDate": "1/22/2020"}
        self.assertTrue(ev.evaluate(ev_test), "Nope")

class TestComposite(unittest.TestCase):
    # TODO test that every logical gate/conjuction behaves as expected
    pass

class TestEngine(unittest.TestCase):
    # TODO test that the Json Eval engine works as expected
    pass 

class TestOperators(unittest.TestCase):
    pass

class TestDateOperations(unittest.TestCase):
    pass


if __name__ == '__main__':
    TestEvaluation.test_lt()
    print("Everything passed")
