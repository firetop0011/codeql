class X(object):
    def __init__(self, arg):
        print("X.__init__", arg)

X(42) # $ tt=X.__init__
print()


class Y(X):
    def __init__(self, arg):
        print("Y.__init__", arg)
        super().__init__(-arg) # $ pt,tt=X.__init__

Y(43) # $ tt=Y.__init__
print()

# ---

class WithNew(object):
    def __new__(cls, arg):
        print("WithNew.__new__", arg)
        inst = super().__new__(cls)
        assert isinstance(inst, cls)
        inst.some_method() # $ MISSING: pt,tt=WithNew.some_method
        return inst

    def __init__(self, arg):
        print("WithNew.__init__", arg)

    def some_method(self):
        print("WithNew.__init__")

WithNew(44) # $ tt=WithNew.__new__ tt=WithNew.__init__
print()


class ExtraCallToInit(object):
    def __new__(cls, arg):
        print("ExtraCallToInit.__new__", arg)
        inst = super().__new__(cls)
        assert isinstance(inst, cls)
        # you're not supposed to do this, since it will cause the __init__ method will be run twice.
        inst.__init__(1001) # $ MISSING: pt,tt=ExtraCallToInit.__init__
        return inst

    def __init__(self, arg):
        print("ExtraCallToInit.__init__", arg, self)

ExtraCallToInit(1000) # $ tt=ExtraCallToInit.__new__ tt=ExtraCallToInit.__init__
print()


class InitNotCalled(object):
    """as described in https://docs.python.org/3/reference/datamodel.html#object.__new__
    __init__ will only be called when the returned object from __new__ is an instance of
    the `cls` parameter...
    """
    def __new__(cls, arg):
        print("InitNotCalled.__new__", arg)
        return False

    def __init__(self, arg):
        print("InitNotCalled.__init__", arg)

InitNotCalled(2000) # $ tt=InitNotCalled.__new__ SPURIOUS: tt=InitNotCalled.__init__
print()