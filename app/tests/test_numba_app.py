import unittest

class TestPIV(unittest.TestCase):

    def test_cold_start(self):
        try:
            cold_start()
        except Exception as e:
            self.fail(f"Cold start failed: {e}")

    def test_piv_output(self):
        image_a = np.random.random((32, 32))
        image_b = np.random.random((32, 32))
        u, v = compute_piv(image_a, image_b, 8)
        self.assertEqual(u.shape, image_a.shape)
        self.assertEqual(v.shape, image_a.shape)

if __name__ == '__main__':
    unittest.main()
