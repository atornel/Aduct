import unittest
import Aduct
from Aduct import Gtk


def new_element():
    element = Aduct.Element()
    return element


class TestNotebook(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = None
        self.notebook = None

    def setUp(self):

        self.element = new_element()
        self.notebook = Aduct.Notebook()

    def tearDown(self):

        self.element.destroy()
        self.notebook.destroy()
        self.element = None
        self.notebook = None

    def test_add_child(self):

        self.notebook.add_child(self.element)
        self.assertEqual(self.notebook.get_nth_page(0), self.element)

    def test_add_child_err(self):

        wid = Gtk.Grid()
        self.assertRaises(TypeError, self.notebook.add_child, wid)

    def test_change_child_label_1(self):

        self.notebook.add_child(self.element)
        self.element.child_name = "Name"
        self.notebook.change_child_label(self.element)
        label = self.notebook.get_tab(self.element)
        self.assertEqual(label.get_text(), "Name")

    def test_change_child_label_2(self):

        self.notebook.add_child(self.element)
        self.notebook.change_child_label(self.element)
        label = self.notebook.get_tab(self.element)
        self.assertEqual(label.get_text(), "No child")

    def test_get_action_button_1(self):

        icon = Gtk.Image.new_from_icon_name("terminal", 2)
        self.notebook.set_action_button(icon, 0)
        but = self.notebook.get_action_button(0)
        n_icon = but.get_child()
        self.assertEqual(icon, n_icon)

    def test_get_action_button_2(self):

        icon = Gtk.Image.new_from_icon_name("terminal", 2)
        self.notebook.set_action_button(icon, 1)
        but = self.notebook.get_action_button(1)
        n_icon = but.get_child()
        self.assertEqual(icon, n_icon)

    def test_get_tab_1(self):

        self.element.child_name = "Name"
        tab = self.notebook.get_tab(self.element)
        self.assertEqual(tab.get_text(), "Name")

    def test_get_tab_2(self):

        tab = self.notebook.get_tab(self.element)
        self.assertEqual(tab.get_text(), "No child")

    def test_get_props(self):

        self.notebook.add_child(self.element)
        self.notebook.add_child(new_element())
        exp_props = {
            "type": "notebook",
            "tab_position": 2,
            "n_action_button": 0,
            "element_0": {"type": "element", "provider": None, "child": {}},
            "element_1": {"type": "element", "provider": None, "child": {}},
            "n_elements": 2,
        }
        obs_props = self.notebook.get_props()
        self.assertEqual(exp_props, obs_props)

    def test_remove_child(self):

        self.notebook.add_child(self.element)
        self.notebook.remove_child(self.element)
        self.assertNotIn(self.element, self.notebook)

    def test_remove_child_err(self):

        self.assertRaises(ValueError, self.notebook.remove_child, self.element)

    def test_replace_child(self):

        n_element = new_element()
        self.notebook.add_child(self.element)
        self.notebook.replace_child(self.element, n_element)
        self.assertEqual(self.notebook.get_nth_page(0), n_element)

    def test_replace_child_err_1(self):

        n_element = new_element()
        self.assertRaises(
            ValueError, self.notebook.replace_child, self.element, n_element
        )

    def test_replace_child_err_1(self):

        wid = Gtk.Grid()
        self.notebook.add_child(self.element)
        self.assertRaises(TypeError, self.notebook.replace_child, self.element, wid)

    def test_set_action_button_1(self):

        icon = Gtk.Image.new_from_icon_name("terminal", 2)
        self.notebook.set_action_button(icon, 1)
        but = self.notebook.get_action_widget(1)
        n_icon = but.get_child()
        self.assertEqual(icon, n_icon)

    def test_set_action_button_1(self):

        icon = Gtk.Image.new_from_icon_name("terminal", 2)
        self.notebook.set_action_button(icon, 1)
        but = self.notebook.get_action_widget(1)
        n_icon = but.get_child()
        self.assertEqual(icon, n_icon)

    def test_set_from_props(self):

        element_0 = new_element()
        element_1 = new_element()

        props = {
            "type": self.notebook,
            "tab_position": 2,
            "n_action_button": 0,
            "element_0": {"type": element_0, "provider": None, "child": {}},
            "element_1": {"type": element_1, "provider": None, "child": {}},
            "n_elements": 2,
        }

        self.notebook.set_from_props(props)
        elements = (self.notebook.get_nth_page(0), self.notebook.get_nth_page(1))
        exp_elements = (element_0, element_1)
        self.assertEqual(elements, exp_elements)


if __name__ == "__main__":
    unittest.main()
