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
View can hold children of type :mod:`.Element`. In some case, there is a
restriction on number of children it can hold.
"""


class View:
    def __init__(self, **kwargs):

        """
        This an abstract class, that gives an idea of methods a :mod:`.View` must have.
        Unless otherwise stated, all the description of methods are generalised expected behavior of
        :mod:`.View`. Depending upon the nature of view, the type of child it can hold also varies.
        """

        pass

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
            Raised when there is insufficient information to add :obj:`child` to :obj:`self`.

        TypeError
            Raised when :obj:`child` is of invalid type.

        Note
        ----
        When there is a lack of information to add :obj:`child`, :obj:`self` may try its best to add
        :obj:`child` in suitable position.
        """

        pass

    def get_props(self):

        """
        Gets the interface properties.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties.
        """

        pass

    def get_type(self):

        """
        Gets the interface properties.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties.
        """

        return self.get_property("type")

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
            Raises when :obj:`child` is not present in :obj:`self`.
        """

        pass

    def replace_child(self, old_child, new_child):

        """
        Replaces the existing child with new child.

        Arguments
        ---------
        old_child : :mod:`.View` or :mod:`.Element`
            The child present in :obj:`self` which has to be replaced.
        new_child : :mod:`.View` or :mod:`.Element`
            The child that will replace `old_child` of :obj:`self`.
        """

        pass

    def set_from_props(self, props):

        """
        Sets the interface from given properties.

        Arguments
        ---------
        props : :class:`dict`
            The dictionary containig properties of interface.
        """

        pass
