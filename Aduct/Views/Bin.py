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
Bin is a view that can hold only one child. The child can be either an :mod:`.View` or
:mod:`.Element`.
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Bin(Gtk.Bin):
    def __init__(self, **kwargs):

        """
        Makes a bin based on given properties.

        Arguments
        ---------
        **kwargs
            The keyword arguments to be passed to :class:`Gtk.Bin` from which :mod:`.Bin` is made.
        """

        super().__init__(**kwargs)
        if not kwargs.get("name", False):
            self.set_name("aduct-bin")
        self.type = "bin"

    def add_child(self, child):

        """
        Adds the child :obj:`self`.

        Arguments
        ---------
        child : :mod:`.View` or :mod:`.Element`
            The child to be added to :obj:`self`.

        Raises
        ------
        ValueError
            Raised when :obj:`self` already has a child.
        """

        if self.get_child():
            raise ValueError("Aduct.Bin cannot have any more child")
        self.add(child)

    def get_props(self):

        """
        Gets the interface properties.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties.
        """

        props = {"type": "bin"}
        child = self.get_child()
        if child:
            child_props = child.get_props()
            props["child"] = child_props
        else:
            props["child"] = {}
        return props

    def remove_child(self, child):

        """
        Removes the given child.

        Arguments
        ---------
        child : :mod:`.View` or :mod:`.Element`
            The child which has to be removed from :obj:`self`.

        Raises
        ------
        ValueError
         Raised when :obj:`child` is not present in :obj:`self`.
        """

        if child == self.get_child():
            self.remove(child)
        else:
            raise ValueError("Child is not in Aduct.Bin")

    def replace_child(self, old_child, new_child):

        """
        Replaces the existing child with a new child.

        Arguments
        ---------
        old_child : :mod:`.View` or :mod:`.Element`
            The child present in :obj:`self` which has to be replaced.
        new_child : :mod:`.View` or :mod:`.Element`
            The child that will replace the given :obj:`old_child` of :obj:`self`.
        """

        self.remove_child(old_child)
        self.add(new_child)

    def set_from_props(self, props):

        """
        Sets the interface from given properties.

        Arguments
        ---------
        props : :class:`dict`
            The dictionary containig properties of interface.
        """

        child_props = props["child"]
        if not child_props:
            return
        child = child_props["type"]
        self.add(child)
        child.set_from_props(child_props)
