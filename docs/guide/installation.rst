Installation
============

Simply put, to use Aduct, you need to install it. The following guide
should be able help you in getting Aduct. For advanced users and more
configuration, you are always welcome to grab the source code of Aduct
and do literally whatever you want.

Requirements
------------

Aduct is written in Python and requires Python. Apart from that you
need Gtk, nothing more. So we directly follow the guidelines required to
use Gtk.

-  **Python 3.5+** If not installed, get the latest version of `Python <http://www.python.org>`__.

-  **Gtk 3.0+** The latest version of `Gtk <http://www.gtk.org>`__ is recommended. The instructions to
   install it are highlighted in the official website.

-  **PyGObject** `PyGObject <https://pygobject.readthedocs.io/>`__ provides Python bindings to GI modules (that
   is Gtk and its friends). If this is your first try with Gtk, you may
   have to install it. Directly install it using `PIP <https://pypi.org/project/PyGObject/>`__.

Getting Aduct
--------------

After the requirements are satisfied, installing Aduct won’t be a
trouble. The best way is to install it using PIP.

.. code::

   $ pip install Aduct

As already stated, for those not comfortable with PIP, you can always
get the source code and do necessary things to get Aduct on your
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
