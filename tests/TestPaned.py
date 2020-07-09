import unittest
import Aduct
from Aduct import Gtk


def new_element():
    element = Aduct.Element()
    return element


class TestPaned(unittest.TestCase):

    def setUp(self):

        self.element_1 = new_element()
        self.element_2 = new_element()
        self.paned = Aduct.Paned()

    def tearDown(self):

        self.element_1.destroy()
        self.element_2.destroy()
        self.paned.destroy()

        self.element_1 = None
        self.element_2 = None
        self.paned = None

    def test_add_child(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        children = (self.paned.get_child1(), self.paned.get_child2())
        self.assertEqual(children, (self.element_1, self.element_2))

    def test_add_child_err(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        self.assertRaises(ValueError, self.paned.add_child, new_element())

    def test_get_props(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        exp_props = {
            "type": "paned",
            "child_1": {"type": "element", "provider": None, "child": {}},
            "child_2": {"type": "element", "provider": None, "child": {}},
            "orientation": 0,
            "position": self.paned.get_position(),
        }
        obs_props = self.paned.get_props()

        self.assertEqual(exp_props, obs_props)

    def test_remove_child(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        self.paned.remove_child(self.element_2)
        children = (self.paned.get_child1(), self.paned.get_child2())
        self.assertEqual(children, (self.element_1, None))

    def test_remove_child_err(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        n_element = new_element()
        self.assertRaises(ValueError, self.paned.remove_child, n_element)

    def test_replace_child(self):

        self.paned.add_child(self.element_1)
        self.paned.add_child(self.element_2)

        n_element = new_element()

        self.paned.replace_child(self.element_1, n_element)
        children = (self.paned.get_child1(), self.paned.get_child2())
        self.assertEqual(children, (n_element, self.element_2))

    def test_replace_child_err(self):

        self.paned.add_child(self.element_1)
        n_element = new_element()

        self.assertRaises(
            ValueError, self.paned.replace_child, self.element_2, n_element
        )

    def test_set_from_props(self):

        props = {
            "type": self.paned,
            "child_1": {"type": self.element_1, "provider": None, "child": {}},
            "child_2": {"type": self.element_2, "provider": None, "child": {}},
            "orientation": 0,
            "position": 20,
        }
        self.paned.set_from_props(props)
        exp_vals = (self.element_1, self.element_2, 0, 20)
        obs_vals = (
            self.paned.get_child1(),
            self.paned.get_child2(),
            self.paned.get_orientation(),
            self.paned.get_position(),
        )
        self.assertEqual(exp_vals, obs_vals)


if __name__ == "__main__":
    unittest.main()
