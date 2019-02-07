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
    def test_list_contacts(self):
        self.assertEqual(len(eab.list_contacts(100, 0)), 100)
        self.assertNotEqual(eab.list_contacts(100,0), eab.list_contacts(100,1))
        self.assertEqual(list(set(eab.list_contacts(100,0)) & set(eab.list_contacts(100,1))), [])
        self.assertEqual(list(set(eab.list_contacts(100,0)) & set(eab.list_contacts(50,1))), [])
        self.assertNotEqual(eab.list_contacts(20,0)[2].name, None)
    def test_bad_data_types(self):
        self.assertRaises(TypeError, eab.add_contact, 'string' , 2 , 3)
        self.assertRaises(TypeError, eab.add_contact, 1 , 'string' , 3)
        self.assertRaises(TypeError, eab.add_contact, 1 , 2 , 'string')
        self.assertRaises(TypeError, eab.add_contact, 'string' , 'string' , 3)
        self.assertRaises(TypeError, eab.add_contact, 'string' , 2 , 'string')
        self.assertRaises(TypeError, eab.add_contact, 1 , 'string' , 'string')
        self.assertRaises(TypeError, eab.delete_contact, 1)
        self.assertRaises(TypeError, eab.delete_contact, 1.0)
        self.assertRaises(TypeError, eab.update_contact, 'string' , 2 , 3)
        self.assertRaises(TypeError, eab.update_contact, 1 , 'string' , 3)
        self.assertRaises(TypeError, eab.update_contact, 1 , 2 , 'string')
        self.assertRaises(TypeError, eab.update_contact, 'string' , 'string' , 3)
        self.assertRaises(TypeError, eab.update_contact, 'string' , 2 , 'string')
        self.assertRaises(TypeError, eab.update_contact, 1 , 'string' , 'string')
        self.assertRaises(TypeError, eab.list_contacts, 'string', 'other string')
        self.assertRaises(TypeError, eab.search_contact, 1)
        self.assertRaises(TypeError, eab.has, 1)
    def test_too_big(self):
        self.assertRaises(Exception, eab.add_contact, 
        'lzvicpghimacvfaizmkfkshiivuyjwlqfxnyxxpskpgyznrksjdnurwdtdkxazbisflefdxsahhiyxdviosulmrjwrbrxjntxtytf', 
        'nmapugnwshpshzzraaupbeuaadwsmoqqkdnvosudhthskvawogwjzqashpaqkiijmnnpwxugcrmkutklpkzwxmkkhnhdlmrrqiildzozmkhmydydcwbculceybbbafjoxtgmcjsjhyfrpbobrafhwii', 
        '5529533362262178')
        self.assertRaises(Exception, eab.update_contact, 
        'lzvicpghimacvfaizmkfkshiivuyjwlqfxnyxxpskpgyznrksjdnurwdtdkxazbisflefdxsahhiyxdviosulmrjwrbrxjntxtytf', 
        'nmapugnwshpshzzraaupbeuaadwsmoqqkdnvosudhthskvawogwjzqashpaqkiijmnnpwxugcrmkutklpkzwxmkkhnhdlmrrqiildzozmkhmydydcwbculceybbbafjoxtgmcjsjhyfrpbobrafhwii', 
        '5529533362262178')
        self.assertRaises(Exception, eab.search_contact, 
        'lzvicpghimacvfaizmkfkshiivuyjwlqfxnyxxpskpgyznrksjdnurwdtdkxazbisflefdxsahhiyxdviosulmrjwrbrxjntxtytf')
        self.assertRaises(Exception, eab.delete_contact, 
        'lzvicpghimacvfaizmkfkshiivuyjwlqfxnyxxpskpgyznrksjdnurwdtdkxazbisflefdxsahhiyxdviosulmrjwrbrxjntxtytf')
    def tearDown(self):
        eab.delete_contact('Zulu Fakename')
        eab.delete_contact('string')
if __name__ == '__main__':
    unittest.main()
    