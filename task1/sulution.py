"""Необходимо реализовать декоратор @strict
Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе функции.
(подсказка: аннотации типов аргументов можно получить из атрибута объекта функции func.__annotations__ или с помощью модуля inspect)
При несоответствии типов бросать исключение TypeError
Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int, float, str
Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию"""

def strict(func):
    def wrapper(*args, **kwargs):
        for arg, key in zip(args, func.__annotations__):
            if not isinstance(arg, func.__annotations__[key]):
                raise TypeError("Неверный тип данных")
        
        result = func(*args, **kwargs)

        if not isinstance(result, func.__annotations__['return']):
            raise TypeError("Возвращаемое значение не соответствует ожидаемому типу")
        
        return result
    
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
