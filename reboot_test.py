import unittest

from reboot import RebootFormParser


class RebootTest(unittest.TestCase):
    def test_token_parse(self):
        parser = RebootFormParser()
        with open("test.html", 'r') as f:
            parser.feed(f.read())
        self.assertEqual(parser.get_token(), "/apply.cgi?/reboot_waiting.htm timestamp=1048576")


if __name__ == '__main__':
    unittest.main()
