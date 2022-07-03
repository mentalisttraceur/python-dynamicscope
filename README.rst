Dynamic Scope in Python
=======================

This module implements dynamic scope for Python: it allows Python code
to get and set variables defined anywhere in its call stack, searching
first its own local variables, then its caller's local variables, and
so on, until it finds a variable with the desired name.

It is strongly recommended to only use this module for education, fun
party tricks, and write-only throw-away code which no one will ever
need to reuse or maintain.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install dynamicscope


Usage
-----

Import:

.. code:: python

    from dynamicscope import DYNAMIC_SCOPE

To get a variable named ``x`` in the current dynamic scope:

.. code:: python

    DYNAMIC_SCOPE.x

(**Note:** dynamic scope starts with *your* stack frame, not your caller's
stack frame, so if you have a variable named ``x`` in the local scope,
``DYNAMIC_SCOPE.x`` will refer to that ``x``, not bypass it.)

To overwrite a existing variable named ``x`` in the current dynamic scope:

.. code:: python

    DYNAMIC_SCOPE.x = 'foo'

To delete a variable named ``x`` found in the current dynamic scope:

.. code:: python

    del DYNAMIC_SCOPE.x

(**DANGER:** reaching up from a lower scope to delete variables in
callers is a GOTO-level crime under international software law.)

If a variable is not found in dynamic scope, an ``AttributeError`` is raised:

.. code::

    AttributeError: 'x' not found in dynamic scope

(It is an ``AttributeError`` and not a ``NameError`` because dynamic scope
is accessed with attribute access - returning the standard error for
attribute access composes better with existing code and builtins like
``hasattr``, ``getattr``, and ``delattr``.)

Getting and setting variables with dynamic scope is not always possible
in Python. Two errors, both subclasses of ``RuntimeError``, are defined
to help you detect when it cannot be done:

* If the stack cannot be inspected to find variables during either
  a get, set, or delete: a ``dynamicscope.ReadError`` is raised.

* If the stack cannot be modified during a set or delete:
  a ``dynamicscope.WriteError`` is raised.

Caution
~~~~~~~

**Most languages to not have dynamic scope for really good reason.**

In a world where dynamic scope is used, *your local variables are part
of your observable interface*, and the only thing protecting two
pieces of code from trampling over or shadowing each others' variables
is conventions about how things are named. For example:

* ``{{your module name}}_foo`` for any variable that you intend for
  your users to set or get through dynamic scope, and

* ``_{{your module name}}_foo`` for any variable that you intend for
  your code to privately set or get through dynamic scope.

Details
~~~~~~~

``dynamicscope`` works by using Python's stack frame inspection, specifically
|currentframe|_ and the ``f_locals`` attribute of `frame objects
<https://docs.python.org/3/reference/datamodel.html#frame-objects>`_.

.. |currentframe| replace:: ``inspect.currentframe()``
.. _currentframe:
    https://docs.python.org/3/library/inspect.html#inspect.currentframe
