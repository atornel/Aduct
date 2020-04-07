# Package : Quanta Tool Kit (Qtk)
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
Paned is a view that can hold two children. The two children can either be :mod:`.View` or
:mod:`.Element`.
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Paned(Gtk.Paned):
    def __init__(self, **kwargs):

        """
        Makes a paned based on given properties.

        Arguments
        ---------
        **kwargs
            The keyword arguments to be passed to :class:`Gtk.Paned` from which :mod:`.Paned` is
            made.
        """

        super().__init__(**kwargs)
        if not kwargs.get("name", False):
            self.set_name("qtk-paned")
        self.type = "paned"

    def add_child(self, child, position=0):

        """
        Adds the child to paned.

        When :obj:`position` is 1 or 2, :obj:`child` is added at panel 1 or 2 of :obj:`self`
        respectively. When it is 0, :obj:`child` is added to the first available panel. When it is
        neither of specified values, nothing is done.

        Arguments
        ---------
        child : :mod:`.View` or :mod:`.Element`
            The child to be added to :obj:`self`.
        position : :class:`int`
            The panel at which the child has to be added. :obj:`position` can be 0 or 1 or 2, with
            default value being 0.

        Raises
        ------
        ValueError
            Raised when :obj:`self` already has a child.
        """

        if position == 1:
            self.add1(child)
        elif position == 2:
            self.add2(child)
        elif position == 0:
            child1 = self.get_child1()
            child2 = self.get_child2()
            if child1:
                if child2:
                    raise ValueError("Qtk.Paned can not have any more child")
                self.add2(child)
            self.add1(child)

    def get_props(self):

        """
        Gets the interface properties.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties.
        """

        props = {"type": "paned"}
        child_1 = self.get_child1()
        child_2 = self.get_child2()
        if child_1:
            props["child_1"] = child_1.get_props()
        else:
            props["child_1"] = {}
        if child_2:
            props["child_2"] = child_2.get_props()
        else:
            props["child_2"] = {}
        props["orientation"] = self.get_orientation()
        props["position"] = self.get_position()

        return props

    def remove_child(self, child):

        """
        Removes the given child from :obj:`self`.

        Arguments
        ---------
        child : :mod:`.View` or :mod:`.Element`
            The child which has to be removed from :obj:`self`.

        Raises
        ------
        ValueError
            Raised when :obj:`child` is not present in :obj:`self`.
        """

        if child in self.get_children():
            self.remove(child)
        else:
            raise ValueError("Child is not in Qtk.Paned")

    def replace_child(self, old_child, new_child):

        """
        Replaces the existing child with a new child.

        Arguments
        ---------
        old_child : :mod:`.View` or :mod:`.Element`
            The child present in :obj:`self` which has to be replaced.
        new_child : :mod:`.View` or :mod:`.Element`
            The child that will replace the given existing child of :obj:`self`.

        Raises
        ------
        ValueError
            Raised when :obj:`old_child` is not in :obj:`self`.
        """

        child_1 = self.get_child1()
        child_2 = self.get_child2()
        if child_1 is old_child:
            self.remove(child_1)
            self.add1(new_child)
        elif child_2 is old_child:
            self.remove(child_2)
            self.add2(new_child)
        else:
            raise ValueError("Child is not in Qtk.Paned")

    def set_from_props(self, props):

        """
        Sets the interface from given properties.

        Arguments
        ---------
        props : :class:`dict`
            The dictionary containig properties of interface.
        """

        child_1_props = props["child_1"]
        child_2_props = props["child_2"]

        if child_1_props:
            child_1 = child_1_props["type"]
            child_1.set_from_props(child_1_props)
            self.add1(child_1)

        if child_2_props:
            child_2 = child_2_props["type"]
            child_2.set_from_props(child_2_props)
            self.add2(child_2)

        self.set_orientation(props["orientation"])
        self.set_position(props["position"])
