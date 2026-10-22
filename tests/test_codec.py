"""Small protocol checks; no model weights or dataset required."""
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from codec import text_to_bits,bits_to_text


class MessageProtocol(unittest.TestCase):
    def test_shape_and_roundtrip(self):
        for text in ['cv','ab','hi','A']:
            bits=text_to_bits(text)
            self.assertEqual(bits.shape,(32,))
            self.assertEqual(bits_to_text(bits),(text,0))

    def test_three_bit_correction(self):
        for count in range(1,4):
            bits=text_to_bits('cv')
            bits[:count]=1-bits[:count]
            self.assertEqual(bits_to_text(bits),('cv',count))

    def test_ascii_limits(self):
        for text in ['','abc','\u4e2d']:
            with self.assertRaises(ValueError):
                text_to_bits(text)

    def test_invalid_prediction(self):
        with self.assertRaises(ValueError):
            bits_to_text(np.zeros(20))
        with self.assertRaises(ValueError):
            bits_to_text(np.full(32,np.nan))


if __name__=='__main__':
    unittest.main()
