import unittest

from clientwrapper import BasicMapping


class MappingTestCase(unittest.TestCase):
    def test_filtering(self):
        apples_data = [
            {
                'color': 'red',
                'taste': 'sweet'
            },
            {
                'color': 'green',
                'taste': 'sour'
            },
            {
                'color': 'purple',
                'taste': 'rotten'
            }
        ]
        apples = list(map(BasicMapping, apples_data))
        kept_apples = list(filter(lambda apple: apple['taste'] != 'rotten', apples))
        self.assertEqual(len(kept_apples), 2)
        removed_apples = list(filter(lambda apple: apple['color'] == 'purple', apples))
        self.assertEqual(len(removed_apples), 1)
