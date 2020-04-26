# Package : Aduct
# Author : J Arun Mani
# Copyright (C) 2020  J Arun Mani; Atornel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Element represents an individual block. It can hold a widget and handle operations with it.
While setting and removing, a ``child_dict`` named dictionary is taken and returned.
The format of ``child_dict`` is as follows

.. code:: python

   child_dict = {
       "child": Gtk.Widget,
       "child_name": str,
       "icon": Gtk.Image,
       "header_child": Gtk.Widget or None,
       "provider": Aduct.Provider
   }

Here only ``header_child`` key is optional.


"""
import gi

gi.require_versions({"Gtk": "3.0"})
from gi.repository import Gtk


class Element(Gtk.Bin):

    __gsignals__ = {
        "action-clicked": (2, None, (Gtk.Button, int)),
        "child-added": (2, None, ()),
        "child-cleared": (2, None, ()),
        "child-removed": (2, None, ()),
    }

    def __init__(self, child_dict=None, use_action_button=True, pack_type=0, **kwargs):

        """
        Makes an element based on given properties. Its CSS name is *aduct-element*.

        Arguments
        ---------
        child_dict : :class:`dict`
            A dictionary object containing properties of child. Given a valid dictionary, the child
            is added to :obj:`self` while initializing. It is :obj:`None`, when not given.
        use_action_button : :class:`bool`
            States whether to use an action button. Default is :class:`True`.
        pack_type : :class:`Gtk.PackType`
            Specfies the position of action button. It can be an integer of value either 0 or 1,
            which represents :class:`Gtk.PackType.START` or :class:`Gtk.PackType.END` respectively.
            The default value is :class:`Gtk.PackType.START`.
        **kwargs
            The values to be passed to :class:`Gtk.Bin`, from which :mod:`.Element` is derived.

        Attributes
        ----------
        action_button : :class:`Gtk.Button`
            Action button that is used to handle interactions with user. Its CSS name is
            *aduct-element-action_button*.
        child_name : :class:`str`
            The name of child held by :obj:`self`.
        header_grid : :class:`Gtk.Grid`
            The grid that is used to hold action button and header child. Its CSS name is
            *aduct-element-header_grid*.
        main_grid : :class:`Gtk.Grid`
            The grid that holds every widget of :obj:`self`. Its CSS name is
            *aduct-element-main_grid*
        pack_type : :class:`Gtk.PackType`
            The position of action button in :obj:`self`.
        provider : :mod:`.Provider`
            The provider that produced the child of :obj:`self`.

        Signals
            action-clicked
                Emitted with an integer when action button of :obj:`self` is
                clicked. The integer is 1, 2, 3 for LMB, MMB, RMB respectively.
            child-added
                Emitted when a child is added to :obj:`self`.
            child-cleared
                Emitted when the child of :obj:`self` is cleared.
            child-removed
                Emitted when the child of :obj:`self` is removed.

        Note
        ----
            Incase having :obj:`use_action_button` as :obj:`False`, an action button is still
            created, but is not attached to the :obj:`self`.
        """

        Gtk.Bin.__init__(self, **kwargs)
        self.set_css_name("aduct-element")

        self.type = "element"
        self.action_button = Gtk.Button()
        self.main_grid = Gtk.Grid()
        self.header_grid = Gtk.Grid()

        self.action_button.set_css_name("aduct-element-action_button")
        self.main_grid.set_css_name("aduct-element-main_grid")
        self.header_grid.set_css_name("aduct-element-header_grid")

        self.pack_type = pack_type

        if child_dict:
            self.set_child(child_dict)
        else:
            self.child_name = None
            self.provider = None

        if use_action_button:
            self.header_grid.attach(self.action_button, self.pack_type, 0, 1, 1)
        self.action_button.connect("button-press-event", self.__handle_event__)
        self.main_grid.attach(self.header_grid, 0, 0, 1, 1)
        self.add(self.main_grid)

    def __add_child__(self, child):

        self.main_grid.attach(child, 0, 1, 1, 1)

    def __handle_event__(self, button, event):

        self.emit("action-clicked", button, event.button)
        return True

    def __remove_child__(self):

        child = self.get_child()
        if not child:
            err = "Aduct.Element has no child"
            raise ValueError(err)
        self.main_grid.remove(child)
        return child

    def __remove_icon__(self):

        icon = self.get_icon()
        if not icon:
            err = "Aduct.Element has no child"
            raise ValueError(err)
        self.action_button.remove(icon)
        return icon

    def __remove_header_child__(self):

        header_child = self.get_header_child()
        if header_child:
            self.header_grid.remove(header_child)
        return header_child

    def clear_child(self):

        """
        Clears the child at :obj:`self`.
        After clearing, :obj:`child-cleared` signal is emitted.
        """

        child_dict = self.remove_child()
        provider = child_dict.pop("provider")
        provider.clear_child(child_dict)
        self.emit("child-cleared")

    def get_child(self):

        """
        Gets the child held by :obj:`self`.

        Returns
        -------
        :class:`Gtk.Widget` or :obj:`None`
            The child of :obj:`self` or :obj:`None` if :obj:`self` has no child.
        """

        return self.main_grid.get_child_at(0, 1)

    def get_child_name(self):

        """
        Gets the name of child held by :obj:`self`.

        Returns
        -------
        :class:`str` or :obj:`None`
            The child name of :obj:`self` or :obj:`None` if :obj:`self` has no child.
        """

        return self.child_name

    def get_header_child(self):

        """
        Gets the child packed at the header of :obj:`self`.

        Returns
        -------
        :class:`Gtk.Widget` or :obj:`None`
            The header child of :obj:`self` or :obj:`None` if :obj:`self` has no header child.
        """

        x_coord = not self.pack_type
        return self.header_grid.get_child_at(x_coord, 0)

    def get_icon(self):

        """
        Gets the icon representing child held by :obj:`self`.

        Returns
        -------
        :class:`Gtk.Image` or :obj:`None`
            The icon of :obj:`action_button` or :obj:`None` if :obj:`self` has no icon for child.
        """

        return self.action_button.get_child()

    def get_props(self):

        """
        Gets the properties of child held by :obj:`self`.

        Returns
        -------
        :class:`dict`
            The dictionary that can be later used to build the same interface.
        """

        props = {"type": "element"}
        if self.child_name:
            child_props = self.provider.get_child_props(
                self.child_name, self.get_child(), self.get_header_child()
            )
            props["provider"] = self.provider.name
            props["child"] = child_props
        else:
            props["provider"] = None
            props["child"] = {}
        return props

    def get_provider(self):

        """
        Gets the provider for child held by :obj:`self`.

        Returns
        -------
        :mod:`.Provider` or :obj:`None`
            The provider of :obj:`self` or :obj:`None` if :obj:`self` has no child.
        """

        return self.provider

    def remove_child(self):

        """
        Removes the child held by :obj:`self`.

        By removing a child, all its associated properties like icon, header child are also
        removed.
        A :obj:`child-removed` signal is emitted by :obj:`self` after removal.

        Raises
        ------
        ValueError
            Raised when :obj:`self` has no child.

        Returns
        -------
        :class:`dict`
            A dictionary with child properties.
        """

        if not self.child_name:
            err = "Aduct.Element has no child"
            raise ValueError(err)

        child_dict = {}

        child_dict["child_name"] = self.child_name
        child_dict["provider"] = self.provider

        child_dict["child"] = self.__remove_child__()
        child_dict["icon"] = self.__remove_icon__()
        child_dict["header_child"] = self.__remove_header_child__()

        self.child_name = None
        self.provider = None

        self.emit("child-removed")

        return child_dict

    def set_child(self, child_dict):

        """
        Sets the child in :obj:`self` from given properties.

        If :obj:`self` already has a child, then its cleared before adding this new child.
        A :obj:`child-added` signal is emitted after addition.

        Arguments
        ---------
        child_dict : :class:`dict`
            A valid dictionary with properties of child.
        """

        if self.child_name:
            self.clear_child()

        child = child_dict.get("child")
        child_name = child_dict.get("child_name")
        icon = child_dict.get("icon")
        provider = child_dict.get("provider")
        header_child = child_dict.get("header_child", None)

        self.__add_child__(child)
        self.set_child_name(child_name)
        self.set_icon(icon)
        self.set_provider(provider)

        if header_child:
            self.set_header_child(header_child)

        self.main_grid.show_all()
        self.emit("child-added")

    def set_from_props(self, props):

        """
        Sets the interface of :obj:`self` from given properties.

        If :obj:`self` already has a child, then its cleared before adding this new child.

        Arguments
        ---------
        props : :class:`dict`
            The dictionary from which properties are set.
        """

        provider = props["provider"]
        if not provider:
            return

        child_props = props["child"]
        child_dict = provider.get_child_from_props(child_props)
        child_dict["child_name"] = child_props["child_name"]
        child_dict["provider"] = provider

        self.set_child(child_dict)

    def set_child_name(self, child_name):

        """
        Sets the name of child held by :obj:`self`.

        Arguments
        ---------
        child_name : :class:`str`
            The new name of child.
        """

        self.child_name = child_name

    def set_header_child(self, header_child):

        """
        Sets the header child of :obj:`self`.

        Arguments
        ---------
        header_child : :class:`Gtk.Widget`
            The new header child of :obj:`self`.
        """

        self.header_grid.attach(header_child, not self.pack_type, 0, 1, 1)

    def set_icon(self, icon):

        """
        Sets the icon of child held by :obj:`self`.

        Arguments
        ---------
        icon : :class:`Gtk.Image`
            The new icon of child.
        """

        self.action_button.add(icon)

    def set_provider(self, provider):

        """
        Sets the provider of child held by :obj:`self`.

        Arguments
        ---------
        provider : :class:`.Provider`
            The new provider of child.
        """

        self.provider = provider
