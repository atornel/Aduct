Introduction
============

Quanta Tool Kit (Qtk) is a toolkit to design graphical applications that can be
dynamically changed with a little work as possible. It is designed by
inheriting objects provided by `Gtk <http://www.gtk.org>`__ and thus by
following principles of Qtk with Gtk, one can make powerful
applications that are easy for a developer to develop, third-party
person to improve and end user to use.

The Need
--------

Let us assume you make an amazing application. As its core developer,
you design the interface in such a way that it looks awesome to you. In
other words, it has an interface that reflects your ideas on how a
graphical user interface should look. Apart from the code (which nobody
cares when your application is closed-source), the *where and how*
widgets are arranged in the user interface is also important (which
everybody cares except you).

After designing the application, naturally you get more comfortable with
the interface, so it doesn’t look strange to you in any way. But this isn't
the case with users. There are also certain challenges that you often need
to overcome after publishing or improving the application :

-  **You need to add a feature**
   New features become a nightmare when it involves a lot of rewrites. The
   problem with adding the new feature is the doubt if it will be accepted
   by users or whether they will work properly with other parts of application.

-  **Allowing third-party plugins**
   The developer of the plugin may not have the same thinking you do.
   Sometimes by mistake, they completely spoil the working of your application.
   Also a plugin is not always cooperative with other plugins. It may inhibit
   the working of other plugins.

-  **Impressing the users**
   Unfortunately there is also a good chance that your users may be totally
   against the interface of your application. For them, you need to have an
   interface that can be changed at their will. Some applications may even
   have a different layout of interface for each file. So you need to make
   an application whose interface can literally be saved and ported.

How can you tackle these hurdles? Let us try to describe the *sudden
solutions* that comes to your mind.

For the first issue, the complexity depends on your code and interface.
Depending on that, adding a new feature could be simple as adding a few
lines of code or a complete rewrite of your entire application. But what
if you want a solution that doesn’t depend on the complexity of your
application?

The second issue can be avoided by dividing your application interface
into loosely coupled parts. Then you allow the plugins to affect only
certain parts of the application. Mostly it is some panel situated at
one edge of the application, where the plugin gets its place. In other
words, you place a restriction on the scope of a plugin, so that it
doesn’t interfere with other blocks of application. If a plugin wants a
central representation in your application, how can you achieve that?
Can you design an approach that gives your plugin all the essential
freedom?

The issue with users is the most important one to take care. To make an
interface that can be easily changed by users is the most irritating.
Sorting out the requirements, checking whether a feature *will be useful or not*
is also difficult to resolve. For you, placing the toolbox at right
seems plausible, but there could be a creepy user who wants it at
bottom. Possibilities exist. Saving the interface is another headache.
*Which widget was modified ?*, *which should be saved ?*, *how to save
?*, all questions makes you *think*.

There are more such issues which doesn’t go easy with a developer.

A Solution
----------

Qtk can be used to kick-out the above mentioned issues. Some
developers may be think that such issues can be avoided by writing a few
more lines of code. And yes, Qtk is such a package made with a few
lines of code. It is very small, but when you follow its approach, it
saves your essential time and resources, which can be instead used in
improving other concepts of your application.

Qtk’s design principle is very simple. You make widgets that are
independent of each other. Make a basic layout of the interface, then
sit back and relax, because Qtk now takes care of other requirements.
We believe in *“take care of small things and big things will
automatically be taken care”*. It should not be hidden that at first you
may have trouble writing independent widgets, but once you are able to
make one, then you hardly need to focus in its working with interface.

To The Point
------------

Qtk is inspired by `Blender <http://www.blender.org>`__\ ’s
interface. Blender has such an awesome one where it is possible for a
user to customize it in any way they want. Qtk, which tries to mimic
the behavior, is written in `Python <http://www.python.org>`__ using
Gtk. We will cover the working and making of interfaces with Qtk
later. For now, what you need to understand is that in Qtk, we have
two things that work together. A provider that can produce widgets and a
view, that can hold and display them. Views come with various tweaks,
which just need to be *enabled*. When the requirements of both are
satisfied, you get a good interface that can suit all the use cases. The
description so far may seem so absurd and you may not have even able to
get a single point. It’s okay, continue reading, you will *understand*.
