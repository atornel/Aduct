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
Provider acts as a producer of widgets that are placed as child in :mod:`.Element`.
"""

from gi.repository import GObject


class Provider(GObject.Object):
    def __init__(self, *args, **kwargs):

        """
        This a template that gives an idea of methods a :mod:`.Provider` must have.
        Unless otherwise stated, all the description of methods are generalised expected behavior of
        a :mod:`.Provider`.
        """

        GObject.Object.__init__(self, *args, **kwargs)

    def clear_child(self, child_dict):

        """
        Clears the given child.

        Arguments
        ---------
        child_dict: :class:`dict`
            A dictionary with properties of the child.
        """

        pass

    def get_a_child(self, child_name):

        """
        Gets a child with given name.

        Arguments
        ---------
        child_name : :class:`str`
            The name of child to be retrieved.

        Returns
        -------
        :class:`dict`
            A dictionary with properties of child.
        """

        pass

    def get_child_props(self, child_name, child, header_child):

        """
        Gets the interface properties from given values.

        Arguments
        ---------
        child_name : :class:`str`
            The name of child.
        child : :class:`Gtk.Widget`
            The child produced by :obj:`self`.
        header_child : :class:`Gtk.Widget`
            The header child produced by :obj:`self`.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties of child.
        """

        pass

    def get_child_from_props(self, props):

        """
        Gets a child based on given interface properties.

        Arguments
        ---------
        props : :class:`dict`
            The interface properties for child.

        Returns
        -------
        :class:`dict`
            A dictionary with properties of child.
        """

        pass

    def get_name(self):

        """
        Gets the name of the provider.

        Returns
        -------
        :class:`str`
            The name of provider.
        """

        return self.get_property("name")
