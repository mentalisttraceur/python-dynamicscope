# SPDX-License-Identifier: 0BSD
# Copyright 2022 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Emulate dynamic scope in Python.

This module lets you use dynamic scope in Python. It provides a single
`dynamicscope` object: referring to an attribute on that object will
refer to a variable with the same name, using dynamic scoping rules.
"""

__all__ = ('DYNAMIC_SCOPE',)
__version__ = '1.0.3'


from inspect import currentframe as _currentframe


class ReadError(RuntimeError):
    """The runtime does not support reading variables with dynamic scope."""


class WriteError(RuntimeError):
    """The runtime does not support writing variables with dynamic scope."""


def _find_in_dynamic_scope(name):
    frame = _currentframe()
    if frame is None:
        raise ReadError('need inspectable stack for dynamic scope get')
    sentinel = object()
    frame = frame.f_back.f_back
    while frame is not None:
        value = frame.f_locals.get(name, sentinel)
        if value is not sentinel:
            return value, frame
        frame = frame.f_back
    error = AttributeError(repr(name) + ' not found in dynamic scope')
    try:
        error.name = name
    except AttributeError:
        pass
    raise error


class _DynamicScope(object):
    """This object represents dynamic scope."""

    def __getattribute__(self, name):
        """Get a variable with dynamic scope."""
        return _find_in_dynamic_scope(name)[0]

    def __setattr__(self, name, value):
        """Set a variable with dynamic scope."""
        _find_in_dynamic_scope(name)[1].f_locals[name] = value

    def __delattr__(self, name):
        """Delete a variable with dynamic scope."""
        del _find_in_dynamic_scope(name)[1].f_locals[name]


DYNAMIC_SCOPE = _DynamicScope()


def _dynamic_scope_test():
    # We want to use a reasonably unique variable name here, so that
    # if this test mutation leaks out into outer scope, it doesn't
    # clobber someone's variables. Hence the "_dynamicscope_" prefix.
    _dynamicscope_test_variable = False
    DYNAMIC_SCOPE._dynamicscope_test_variable = True
    return _dynamicscope_test_variable


# If frame locals can be mutated by just changing `.f_locals`, then
# the test returns `True`, and we don't need to do anything else.
# There seems to be consensus in PEP-558 to eventually standardize
# on exactly this behavior, so this code optimistically assumes it.
#
# If this raises an exception, then there is probably a problem
# which makes dynamic scope impossible to support at all, so we
# just let it bubble out during import.
if not _dynamic_scope_test():
    # If the test successfully failed (returned `False` instead of
    # raising an exception), time to try setting up a workaround:
    try:
        from ctypes import c_int as _c_int
        from ctypes import py_object as _py_object
        from ctypes import pythonapi as _pythonapi
        _PyFrame_LocalsToFast = _pythonapi.PyFrame_LocalsToFast
        def _update(frame):
            _PyFrame_LocalsToFast(_py_object(frame), _c_int(1))
    except (ImportError, AttributeError):
        try:
            from __pypy__ import locals_to_fast as _update
        except ImportError:
            def _update(frame):
                del frame
                raise WriteError('need writable stack for dynamic scope set')

    class _DynamicScopeWithForcedUpdates(_DynamicScope):
        def __setattr__(self, name, value):
            """Set a variable with dynamic scope."""
            _, frame = _find_in_dynamic_scope(name)
            frame.f_locals[name] = value
            _update(frame)

        def __delattr__(self, name):
            """Delete a variable with dynamic scope."""
            _, frame = _find_in_dynamic_scope(name)
            del frame.f_locals[name]
            _update(frame)

    DYNAMIC_SCOPE = _DynamicScopeWithForcedUpdates()
