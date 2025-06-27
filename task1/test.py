import pytest

from sulution import strict, sum_two

def test_strict_with_wrong_return():
    @strict
    def foo(a: int) -> str:
        return a
    
    with pytest.raises(TypeError):
        foo(1)

def test_strict_with_right_return():
    @strict
    def foo(a: int) -> int:
        return a
    
    test_var = 1

    assert isinstance(foo(test_var), foo.__annotations__['return'])

def test_sum_two_with_wrong_args():
    with pytest.raises(TypeError):
        sum_two("1", "3")

def test_sum_two_with_right_args():
    assert sum_two(1, 2), 3
