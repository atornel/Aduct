import unittest
import Aduct


def new_element():

    element = Aduct.Element()
    return element


class TestBin(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = None
        self.bin_ = None

    def setUp(self):

        self.element = new_element()
        self.bin_ = Aduct.Bin()

    def tearDown(self):

        self.element.destroy()
        self.bin_.destroy()
        self.bin_ = None
        self.element = None

    def test_add_child(self):

        self.bin_.add(self.element)
        self.assertEqual(self.bin_.get_child(), self.element)

    def test_add_child_err(self):

        self.bin_.add(self.element)
        element_2 = new_element()
        self.assertRaises(ValueError, self.bin_.add_child, element_2)

    def test_get_props(self):

        self.bin_.add(self.element)
        obs_props = self.bin_.get_props()
        exp_props = {
            "type": "bin",
            "child": {"type": "element", "provider": None, "child": {}},
        }
        self.assertEqual(obs_props, exp_props)

    def test_get_props_empty(self):

        obs_props = self.bin_.get_props()
        exp_props = {"type": "bin", "child": {}}
        self.assertEqual(obs_props, exp_props)

    def test_remove_child(self):

        self.bin_.add_child(self.element)
        self.assertEqual(self.bin_.get_child(), self.element)

    def test_remove_child_err(self):

        self.assertRaises(ValueError, self.bin_.remove_child, self.element)

    def test_replace_child(self):

        self.bin_.add(self.element)
        element_2 = new_element()
        self.bin_.replace_child(self.element, element_2)
        self.assertEqual(self.bin_.get_child(), element_2)

    def test_replace_child_err(self):

        element_2 = new_element()
        self.assertRaises(ValueError, self.bin_.replace_child, self.element, element_2)

    def test_set_from_props(self):

        element = new_element()
        props = {
            "type": self.bin_,
            "child": {"type": element, "provider": None, "child": {}},
        }
        self.bin_.set_from_props(props)
        self.assertEqual(self.bin_.get_child(), element)


if __name__ == "__main__":
    unittest.main()
