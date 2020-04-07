import unittest

import Qtk
from Qtk import Gtk


class TestProvider(Qtk.Provider):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.name = name

    def clear_child(self, child_dict):

        name = child_dict["child_name"]
        child = child_dict["child"]
        icon = child_dict["icon"]
        header_child = child_dict["header_child"]

        child.destroy()
        icon.destroy()
        header_child.destroy()

    def get_a_child(self, child_name):

        child_dict = {"child_name": child_name, "provider": self}
        child_dict["child"] = Gtk.Label(label="Test Label")
        child_dict["icon"] = Gtk.Image.new_from_icon_name("test", 2)
        child_dict["header_child"] = Gtk.Label(label="Test Header")

        return child_dict

    def get_child_props(self, child_name, child, header_child):

        props = {
            "child_name": child_name,
            "child_label": child.get_text(),
            "header_label": header_child.get_text(),
        }

        return props

    def get_child_from_props(self, props):

        child = Gtk.Label(label=props["child_label"])
        header_child = Gtk.Label(label=props["header_label"])
        icon = Gtk.Image.new_from_icon_name("test", 2)

        child_dict = {"child": child, "icon": icon, "header_child": header_child}
        return child_dict


prov = TestProvider("Test Provider")


class TestElement(unittest.TestCase):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.element = None

    def setUp(self):

        self.element = Qtk.Element()

    def tearDown(self):

        self.element.destroy()
        self.element = None

    def test_clear_child(self):

        child_dict = prov.get_a_child("Test Child")
        self.element.set_child(child_dict)

        self.element.clear_child()
        self.assertIsNone(self.element.get_child())

    def test_get_props(self):

        child_dict = prov.get_a_child("Test Child")
        self.element.set_child(child_dict)

        exp_props = {
            "type": "element",
            "provider": "Test Provider",
            "child": {
                "child_name": "Test Child",
                "child_label": "Test Label",
                "header_label": "Test Header",
            },
        }
        obs_props = self.element.get_props()
        self.assertEqual(obs_props, exp_props)

    def test_remove_child(self):

        child_dict = prov.get_a_child("Test Child")
        self.element.set_child(child_dict)

        obs_dict = self.element.remove_child()
        self.assertEqual(child_dict, obs_dict)

    def test_set_child(self):

        child_dict = prov.get_a_child("Test Child")
        self.element.set_child(child_dict)

        obs_dict = {
            "child": self.element.get_child(),
            "child_name": self.element.child_name,
            "icon": self.element.get_icon(),
            "provider": self.element.get_provider(),
            "header_child": self.element.get_header_child(),
        }
        self.assertEqual(obs_dict, child_dict)

    def test_set_from_props(self):

        props = {
            "type": self.element,
            "provider": prov,
            "child": {
                "child_name": "Test Child",
                "child_label": "Test Label",
                "header_label": "Test Header",
            },
        }
        self.element.set_from_props(props)
        child_props = prov.get_child_props(
            self.element.child_name,
            self.element.get_child(),
            self.element.get_header_child(),
        )
        obs_props = {"type": self.element, "provider": prov, "child": child_props}
        self.assertEqual(props, obs_props)


if __name__ == "__main__":
    unittest.main()
