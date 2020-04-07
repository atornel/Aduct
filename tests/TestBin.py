import unittest
import Quanta as Qu


def new_element():

    element = Qu.Element()
    return element


class TestBin(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = None
        self.qbin = None

    def setUp(self):

        self.element = new_element()
        self.qbin = Qu.Bin()

    def tearDown(self):

        self.element.destroy()
        self.qbin.destroy()
        self.qbin = None
        self.element = None

    def test_add_child(self):

        self.qbin.add(self.element)
        self.assertEqual(self.qbin.get_child(), self.element)

    def test_add_child_err(self):

        self.qbin.add(self.element)
        element_2 = new_element()
        self.assertRaises(ValueError, self.qbin.add_child, element_2)

    def test_get_props(self):

        self.qbin.add(self.element)
        obs_props = self.qbin.get_props()
        exp_props = {
            "type": "bin",
            "child": {"type": "element", "provider": None, "child": {}},
        }
        self.assertEqual(obs_props, exp_props)

    def test_get_props_empty(self):

        obs_props = self.qbin.get_props()
        exp_props = {"type": "bin", "child": {}}
        self.assertEqual(obs_props, exp_props)

    def test_remove_child(self):

        self.qbin.add_child(self.element)
        self.assertEqual(self.qbin.get_child(), self.element)

    def test_remove_child_err(self):

        self.assertRaises(ValueError, self.qbin.remove_child, self.element)

    def test_replace_child(self):

        self.qbin.add(self.element)
        element_2 = new_element()
        self.qbin.replace_child(self.element, element_2)
        self.assertEqual(self.qbin.get_child(), element_2)

    def test_replace_child_err(self):

        element_2 = new_element()
        self.assertRaises(ValueError, self.qbin.replace_child, self.element, element_2)

    def test_set_from_props(self):

        element = new_element()
        props = {
            "type": self.qbin,
            "child": {"type": element, "provider": None, "child": {}},
        }
        self.qbin.set_from_props(props)
        self.assertEqual(self.qbin.get_child(), element)


if __name__ == "__main__":
    unittest.main()
