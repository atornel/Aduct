Installation
============

Simply put, to use Qtk, you need to install it. The following guide
should be able help you in getting Qtk. For advanced users and more
configuration, you are always welcome to grab the source code of Qtk
and do literally whatever you want.

Requirements
------------

Qtk is written in Python and requires Python. Apart from that you
need Gtk, nothing more. So we directly follow the guidelines required to
use Gtk.

-  **Python 3.5+** If not installed, get the latest version of Python
   from the `website <http://www.python.org>`__.

-  **Gtk 3.0+** The latest version of Gtk is recommended. You can learn
   from the `Gtk website <http://www.gtk.org>`__ how to install the
   stable version.

-  **PyGObject** PyGObject provides Python bindings to GI modules (that
   is Gtk and its friends). If it is your first try with Gtk, you may
   have to install it. Directly install it using PIP (`PyPI
   website <https://pypi.org/project/PyGObject/>`__) or follow the
   instructions from the `official website <https://pygobject.readthedocs.io/>`__.

Getting Qtk
--------------

After the requirements are satisfied, installing Qtk won’t be a
trouble. The best way is to install it using PIP.

.. code::

   $ pip install Qtk

As already stated, for those not comfortable with PIP, you can always
get the source code and do necessary things to get Qtk on your
*PYTHONPATH*.

New to Gtk ?
------------

It might be case, that you don’t even know what is Gtk and perhaps be
wondering how to get started. The following is a quotation from
Wikipedia’s page for Gtk.

   GTK (formerly GTK+ GIMP Toolkit) is a free and open-source
   cross-platform widget toolkit for creating graphical user interfaces
   (GUIs). It is licensed under the terms of the GNU Lesser General
   Public License, allowing both free and proprietary software to use
   it. Along with Qt, it is one of the most popular toolkits for the
   Wayland and X11 windowing systems.
   (Source : `Wikipedia <https://en.wikipedia.org/wiki/GTK>`__)

Learning the basics of Gtk will be easy with Python. To get familiar
with developing Gtk applications, please have a look at the `official
docs <https://www.gtk.org/docs/language-bindings/python/>`__.
