=====
Usage
=====

The ``guitab`` line-oriented command interpreter is the intended user
interface. It is started by running the following from the command line::

   $ guitab

This should display a brief splash screen welcoming you to ``guitab`` and drop
you to a new prompt that looks like this::

   [tab]: 

From there, you execute commands to gradually build up your guitar tab. The
full list of commands can be displayed by typing ``-h<Enter>``.

You can move backwards and forwards in the tab with the commands ``-b`` and
``-f``, respectively. These commands also accept numerical arguments to specify
the number of places to move. After issuing one of these commands, a textual
representation of the tab will be printed out, with a ``*`` character on the
final line indicating where in the tab you currently are.

The whole tab can be printed at anytime (piped through ``less``) with the
``-p`` command.

Chords are added with the command ``-c [list of fret numbers]``. 

---
API
---

If instead you want a Python object to store and manipulate tab data, you can
use the :class:`Tab <guitab.tab.Tab>` class. Basic usage along the lines:

.. code-block:: python

   from guitab.tab import Tab

   my_tab = Tab()
   # manipulate tab object as needed
