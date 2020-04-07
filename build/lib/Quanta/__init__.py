# Package : Quanta
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

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Quanta.Element import Element
from Quanta.Provider import Provider
from Quanta.Views import Bin, Paned, Notebook, View


def add_to_notebook(element, notebook, position=-1):

    """
    Adds an element to the notebook at given position.

    When the given :obj:`element` is already a child of some container, the function removes it from
    the parent and adds the :obj:`notebook` to parent. Then the orphan :obj:`element` is added to
    :obj:`notebook` at :obj:`position`.

    Arguments
    ---------
    element : :mod:`.Element`
        The element to be added to `notebook`.
    notebook : :mod:`.Notebook`
        The notebook to which :obj:`element` has to be added
    position : :class:`int`
        The position at which :obj:`element` has to be inserted. When not provided, it takes up
        value of -1, which inserts the element as last page.

    Raises
    ------
    :class:`TypeError`
        When given :obj:`element` is not a :mod:`.Element`.
    """
    try:
        type_ = element.type
    except AttributeError:
        raise TypeError(Notebook.INVALID_CHILD)

    if type_ != "element":
        raise TypeError(Notebook.INVALID_CHILD)

    parent = element.get_parent()
    if parent:
        parent.replace_child(element, notebook)
        notebook.add_child(element, position)
        parent.show_all()
    else:
        notebook.add_child(element, position)


def add_to_paned(child1, child2, paned, position):

    """
    Adds the children to given paned determined by position.

    The main child :obj:`child1` is added at first panel if :obj:`position` is 1 or second panel if
    :obj:`position` is 2. With respect to position of :obj:`child1`, :obj:`child2` is added at the
    complement panel. When :obj:`position` is neither 1 nor 2, nothing is done. If :obj:`child1` is
    already a child of parent, it is removed from the parent and :obj:`paned` is added back in its
    position. Then, the orphans :obj:`child1` and :obj:`child2` are added at requred places.

    Arguments
    ---------
    child1 : :class:`Gtk.Widget`
        The main child which has to be added at given :obj:`position`.
    child2 : :class:`Gtk.Widget`
        The other child which has to be added at the complement of given :obj:`position`.
        It has to be an orphan.
    paned : :mod:`.Paned`
        The paned to which the children has to be added.
    position : :class:`int`
        An integer value that is either 1 or 2. The complement of 1 is 2 and vice-versa.
    """

    parent = child1.get_parent()
    if parent:
        parent.replace_child(child1, paned)
    if position == 1:
        paned.add1(child1)
        paned.add2(child2)
    elif position == 2:
        paned.add1(child2)
        paned.add2(child1)

    parent.show_all()


def add_to_view(child, view):

    """
    Adds a child to the view.

    If :obj:`child` is not an orphan, it is removed from its parent and :obj:`view` is added back
    in its place. Then :obj:`child` is added to :obj:`view`.

    Arguments
    ---------
    child : :class:`Gtk.Widget` or Quanta.Element.Element
        The child that has to be added to :obj:`view`. It has to be an orphan.
    view : :mod:`.View` 
        The view to which :obj:`child` has to be added.

    Warning
    -------
        This function is given as a fall-back case and should never be used blindly without knowing
        the properties of :obj:`child` and :obj:`view`. When the :obj:`view` already has a child or
        requires more information about adding it, exceptions are raised. Still, the :obj:`view` may
        try its best to add the :obj:`child` at the possible place, only when it can.

        Incase of :obj:`view` being a :mod:`.Notebook`, it appends the :obj:`child` to the last
        position. But it requires :obj:`child` to be a :mod:`.Element`. So at either case, you still
        have limitations that may end up in a weird result. For the same reasons, :obj:`child` has
        to be an orphan.
    """

    view.add_child(child)
    view.show_all()


def change_child_at_element(element, provider, child_name):

    """
    Changes the child at given element with a child of given name provided by provider.

    The previous child at :obj:`element` is cleared, after which the new child is added.

    Arguments
    ---------
    element : :mod:`.Element`
        The element whose child has to be changed.
    provider : :mod:`.Provider`
        The provider that acts as source of child.
    child_name  : :class:`str`
        The name of child to be added to :obj:`element`.
    """

    child_dict = provider.get_a_child(child_name)
    child_dict["child_name"] = child_name
    child_dict["provider"] = provider
    element.set_child(child_dict)


def get_interface(top_level):

    """
    Gets the interface starting from the given top level.

    Arguments
    ---------
    top_level : :mod:`.View` 
        A view which acts as the root widget.

    Returns
    -------
    :class:`dict`
        A dictionary with properties to build interface.
    """

    interface_props = {**top_level.get_props()}
    return interface_props


def set_interface(interface_dict, top_level, creator_maps, init_maps):

    """
    Sets the interface starting from given the top level.

    Arguments
    ---------
    interface_dict: :class:`dict`
        A dictionary that can be used to set interface.
    top_level: :mod:`.View` 
        The root widget from which the interface has to be set.
    creator_maps : :class:`dict`
        A dictionary of format ``{key: (func, args, kwargs)}``, that is used to create the required
        object. The object is then created using ``func(*args, **kwargs)`` and is substitued as
        value in :obj:`interface_dict` which has key ``key``.
    init_maps : :class:`dict`
        A dictionary of format ``{key: object}`` already initialized objects. The occurences of
        ``key`` in :obj:`inerface_dict` is then replaced with ``object``.

    Returns
    -------
    :class:`Gtk.Widget`
        The widget that was previous child of :obj:`top_level`, :obj:`None` if :obj:`top_level` has
        no child.
    """

    def recursive_replace(dic):

        for key in dic:

            if key in creator_maps:
                name = dic[key]
                obj_creator_func, args, kwargs = creator_maps[key][name]
                obj = obj_creator_func(*args, **kwargs)
                dic[key] = obj

            if key in init_maps:
                val = dic[key]
                dic[key] = init_maps[key][val]

            new_dic = dic[key]
            if isinstance(new_dic, (dict,)):
                recursive_replace(new_dic)

        return dic

    interface_props = recursive_replace(interface_dict)

    new_child = interface_props["type"]
    new_child.set_from_props(interface_props)

    old_child = top_level.get_child()
    if old_child:
        top_level.replace_child(old_child, new_child)

    new_child.show_all()
    return old_child


def remove_element(element, view):

    """
    Removes the given element from view.

    When :obj:`view` is a :mod:`.Bin`, it clears :obj:`element`. For other types of views, it
    removes :obj:`element`. Then, if the number of children in :obj:`view` is one, it replaces
    :obj:`view` with the other child of :obj:`view`.

    Arguments
    ---------
    element : :mod:`.Element`
        The element to be removed.
    view : :mod:`.View` 
        The view from which :obj:`element` has to be removed.
    """

    if view.type == "bin":
        element.clear_child()

    else:
        view.remove_child(element)
        children = view.get_children()
        if len(children) == 1:
            parent = view.get_parent()
            try:
                parent.type in ("bin", "notebook", "paned")
            except AttributeError:
                pass
            else:
                other_child = children[0]
                view.remove_child(other_child)
                parent.replace_child(view, other_child)


def replace_child(view, child1, child2):

    """
    Replaces the given child of a view with another child.

    Arguments
    ---------
    view : :mod:`.View`
        The view whose child has to be replaced.
    child1 : :class:`Gtk.Widget`
        The child of given view which has to be replaced.
    child2 : :class:`Gtk.Widget`
        The child which replaces `child1` in :obj:`view`.

    Raises
    ------
    :class:`TypeError`
        Raised when the given :obj:`view` is not a :mod:`.View`
    """

    try:
        type_ = view.type
    except AttributeError:
        raise TypeError(f"Expected a Quanta.View but got {view}")
    view.replace_child(child1, child2)
