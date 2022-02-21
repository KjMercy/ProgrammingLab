import unittest
from es import CSVFile


class TestCSVFile(unittest.TestCase):

    def test_init(self):
        csvfile = CSVFile('shampoo.txt')
        self.assertEqual(csvfile.name, 'shampoo.txt')
        self.assertIsInstance(csvfile.get_data(), list)

        # chiedi a qualcuno come fare il test dell'eccezione
        # self.assertRaises(Exception, CSVFile(3))
