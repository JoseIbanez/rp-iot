import sys
import unittest

import temp


class TestTempMethods(unittest.TestCase):

    @unittest.skip("demo version")
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_linuxTemp(self):
        ret = temp.read_linuxTemp(".")
        self.assertEqual(37000, ret)

    def test_oregonTemp(self):
        ret = temp.read_oregon("./dev/OS.c1")
        self.assertEqual((32500, 17000), ret)

        ret = temp.read_oregon("./dev/OS.c2")
        self.assertEqual((-2500, 17000), ret)

    def test_ds18b20Temp(self):
        ret = temp.read_ds18b20("./dev/28-0414511765ff-w1_slave")
        self.assertEqual(26062, ret)


if __name__ == '__main__':
    unittest.main()