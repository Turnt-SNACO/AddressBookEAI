import unittest

from ElasticAB import ElasticAB
from Contact import Contact
eab = ElasticAB()


class TestEabMethods(unittest.TestCase):
    def setUp(self):
        eab.delete_contact('Zulu Fakename')
    def test_casing(self):
        self.assertTrue(eab.add_contact('Zulu Fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertFalse(eab.add_contact('zulu fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertFalse(eab.add_contact('zULU fAKENAME', '123 Fake Ln.', '123-456-7890'))
        self.assertTrue(eab.delete_contact('zULU fAKENAME'))
        self.assertTrue(eab.add_contact('zulu fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertTrue(eab.delete_contact('ZULU FAKENAME'))
    def test_add_search_delete(self):
        self.assertTrue(eab.add_contact('Zulu Fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertFalse(eab.add_contact('Zulu Fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertIsInstance(eab.search_contact('Zulu Fakename'), Contact)
        self.assertTrue(eab.delete_contact('Zulu Fakename'))
        self.assertFalse(eab.delete_contact('Zulu Fakename'))
    def test_update(self):
        self.assertTrue(eab.add_contact('Zulu Fakename', '123 Fake Ln.', '123-456-7890'))
        self.assertTrue(eab.update_contact('Zulu Fakename', '123 Real Rd.', '1-1-1'))
        self.assertEqual(eab.search_contact('Zulu Fakename').address, '123 Real Rd.')
        self.assertNotEqual(eab.search_contact('Zulu Fakename').address, '123 Fake Ln.')
        self.assertEqual(eab.search_contact('Zulu Fakename').phone_number, '1-1-1')
        self.assertNotEqual(eab.search_contact('Zulu Fakename').phone_number, '123-456-7890')
        self.assertTrue(eab.delete_contact('Zulu Fakename'))
    def tearDown(self):
        eab.delete_contact('Zulu Fakename')
if __name__ == '__main__':
    unittest.main()
    