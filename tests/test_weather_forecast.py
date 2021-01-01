import unittest
from context import sample

sample += 1

# ToDo Rausfinden, was es damit auf sich hat
unittest.TestCase.setUp()


def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)


def square(x):
    """Return the square of x.

    >>> square(2)
    4
    >>> square(-2)
    5
    """

    return x * x

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print('123')

