import unittest
from appcore.map_model import MapModel

class TestMapModel(unittest.TestCase):

    pass

class TestStationModel(unittest.TestCase):

    def test_x__with_y__expect_z(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMapModel())
    suite.addTest(TestStationModel())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)

