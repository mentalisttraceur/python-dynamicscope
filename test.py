from dynamicscope import DYNAMIC_SCOPE


def test_get_attribute_error():
    try:
        DYNAMIC_SCOPE.not_in_scope
    except AttributeError:
        return
    assert False, 'DYNAMIC_SCOPE.not_in_scope should have raised'


def test_set_attribute_error():
    try:
        DYNAMIC_SCOPE.not_in_scope = 0
    except AttributeError:
        return
    assert False, 'DYNAMIC_SCOPE.not_in_scope = 0 should have raised'


def test_set_attribute_error():
    try:
        del DYNAMIC_SCOPE.not_in_scope
    except AttributeError:
        return
    assert False, 'del DYNAMIC_SCOPE.not_in_scope should have raised'


def test_get_function_local():
    x = 0
    assert DYNAMIC_SCOPE.x == 0


def test_set_function_local():
    x = 0
    DYNAMIC_SCOPE.x = 1
    assert x == 1


def test_delete_function_local():
    x = 0
    del DYNAMIC_SCOPE.x
    try:
        x
    except NameError:
        return
    assert False, 'should have raised'


def test_get_class_local():
    class _TestGetClassLocal(object):
        x = 0
        assert DYNAMIC_SCOPE.x == 0


def test_set_class_local():
    class _TestSetClassLocal(object):
        x = 0
        DYNAMIC_SCOPE.x = 1
        assert x == 1
    assert _TestSetClassLocal.x == 1


def test_delete_class_local():
    class _TestDeleteClassLocal(object):
        x = 0
        del DYNAMIC_SCOPE.x
        try:
            x
        except NameError:
            pass
        else:
            assert False, 'should have raised'
    try:
        _TestDeleteClassLocal.x == 1
    except AttributeError:
        return
    assert False, 'should have raised'


def _test_get_function():
    return DYNAMIC_SCOPE.x


def test_get_function_outside():
    x = 0
    assert _test_get_function() == 0


def _test_set_function():
    DYNAMIC_SCOPE.x = 1


def test_set_function_outside():
    x = 0
    _test_set_function()
    assert x == 1


def _test_delete_function():
    # This deletion of variables from a higher scope is being
    # performed with special authorization under Article 4.2
    # of the Geneva Convention on Programming. Permit #123469
    # to perform these acts for demonstration purposes was
    # duly issued after a full review on July 3rd, 2022.
    del DYNAMIC_SCOPE.x


def test_delete_function_outside():
    x = 0
    _test_delete_function()
    try:
        x
    except NameError:
        return
    assert False, 'should have raised'


def test_get_class_outside():
    class _TestGetClassOutside(object):
        x = 0
        assert _test_get_function() == 0


def test_set_class_outside():
    class _TestSetClassOutside(object):
        x = 0
        _test_set_function()
        assert x == 1


def test_delete_class_outside():
    class _TestDeleteClassOutside(object):
        x = 0
        _test_delete_function()
        try:
            x
        except NameError:
            pass
        else:
            assert False, 'should have raised'
    try:
        _TestDeleteClassOutside.x == 1
    except AttributeError:
        return
    assert False, 'should have raised'


def test_get_function_both_lexical_and_dynamic():
    x = 0
    def _test_get_function_both_lexical_and_dynamic():
        return DYNAMIC_SCOPE.x
    assert _test_get_function_both_lexical_and_dynamic() == 0


def test_set_function_both_lexical_and_dynamic():
    x = 0
    def _test_set_function_both_lexical_and_dynamic():
        DYNAMIC_SCOPE.x = 1
    _test_set_function_both_lexical_and_dynamic()
    assert x == 1


def test_delete_function_both_lexical_and_dynamic():
    x = 0
    def _test_delete_function_both_lexical_and_dynamic():
        del DYNAMIC_SCOPE.x
    _test_delete_function_both_lexical_and_dynamic()
    try:
        x
    except NameError:
        return
    assert False, 'should have raised'


def test_get_class_both_lexical_and_dynamic():
    class _TestGetClassBothLexicalAndDynamic(object):
        x = 0
        def _test_get_class_both_lexical_and_dynamic():
            return DYNAMIC_SCOPE.x
        assert _test_get_class_both_lexical_and_dynamic() == 0


def test_set_class_both_lexical_and_dynamic():
    class _TestSetClassBothLexicalAndDynamic(object):
        x = 0
        def _test_set_class_both_lexical_and_dynamic():
            DYNAMIC_SCOPE.x = 1
        _test_set_class_both_lexical_and_dynamic()
        assert x == 1


def test_delete_class_both_lexical_and_dynamic():
    class _TestDeleteClassBothLexicalAndDynamic(object):
        x = 0
        def _test_delete_class_both_lexical_and_dynamic():
            del DYNAMIC_SCOPE.x
        _test_delete_class_both_lexical_and_dynamic()
        try:
            x
        except NameError:
            pass
        else:
            assert False, 'should have raised'
    try:
        _TestDeleteClassBothLexicalAndDynamic.x == 1
    except AttributeError:
        return
    assert False, 'should have raised'
