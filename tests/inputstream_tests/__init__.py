from __future__ import unicode_literals

from prompt_toolkit.inputstream import InputStream
from prompt_toolkit.keys import Keys

import unittest


class InputStreamTest(unittest.TestCase):
    def setUp(self):
        class _ProcessorMock(object):
            def __init__(self):
                self.keys = []

            def feed_key(self, key_press):
                self.keys.append(key_press)

        self.processor = _ProcessorMock()
        self.stream = InputStream(self.processor)

    def test_control_keys(self):
        self.stream.feed('\x01\x02\x10')

        self.assertEqual(len(self.processor.keys), 3)
        self.assertEqual(self.processor.keys[0].key, Keys.ControlA)
        self.assertEqual(self.processor.keys[1].key, Keys.ControlB)
        self.assertEqual(self.processor.keys[2].key, Keys.ControlP)
        self.assertEqual(self.processor.keys[0].data, '\x01')
        self.assertEqual(self.processor.keys[1].data, '\x02')
        self.assertEqual(self.processor.keys[2].data, '\x10')

    def test_arrows(self):
        self.stream.feed('\x1b[A\x1b[B\x1b[C\x1b[D')

        self.assertEqual(len(self.processor.keys), 4)
        self.assertEqual(self.processor.keys[0].key, Keys.Up)
        self.assertEqual(self.processor.keys[1].key, Keys.Down)
        self.assertEqual(self.processor.keys[2].key, Keys.Right)
        self.assertEqual(self.processor.keys[3].key, Keys.Left)
        self.assertEqual(self.processor.keys[0].data, '\x1b[A')
        self.assertEqual(self.processor.keys[1].data, '\x1b[B')
        self.assertEqual(self.processor.keys[2].data, '\x1b[C')
        self.assertEqual(self.processor.keys[3].data, '\x1b[D')

    def test_escape(self):
        self.stream.feed('\x1bhello')

        self.assertEqual(len(self.processor.keys), 1 + len('hello'))
        self.assertEqual(self.processor.keys[0].key, Keys.Escape)
        self.assertEqual(self.processor.keys[1].key, 'h')
        self.assertEqual(self.processor.keys[0].data, '\x1b')
        self.assertEqual(self.processor.keys[1].data, 'h')

    def test_special_double_keys(self):
        self.stream.feed('\x1b[1;3D') # Should both send escape and left.

        self.assertEqual(len(self.processor.keys), 2)
        self.assertEqual(self.processor.keys[0].key, Keys.Escape)
        self.assertEqual(self.processor.keys[1].key, Keys.Left)
        self.assertEqual(self.processor.keys[0].data, '\x1b[1;3D')
        self.assertEqual(self.processor.keys[1].data, '\x1b[1;3D')
