"""Tests for cached_property.

1. Tests ported from python standard library.
2. Validation for python 3.8+ to use standard library.
"""

# Standard Library
import concurrent.futures
import sys
import threading
import unittest

# Package Implementation
from backports.cached_property import cached_property


class CachedCostItem:
    """Simple cached property with classvar."""

    _cost = 1

    def __init__(self):
        self.lock = threading.RLock()

    @cached_property
    def cost(self):
        """The cost of the item."""
        with self.lock:
            self._cost += 1
        return self._cost


class OptionallyCachedCostItem:
    """Cached property with non-cached getter available."""

    _cost = 1

    def get_cost(self):
        """The cost of the item."""
        self._cost += 1
        return self._cost

    cached_cost = cached_property(get_cost)


class CachedCostItemWait:
    """Cached property with waiting for event."""

    def __init__(self, event):
        self._cost = 1
        self.lock = threading.RLock()
        self.event = event

    @cached_property
    def cost(self):
        """The cost of the item."""
        self.event.wait(1)
        with self.lock:
            self._cost += 1
        return self._cost


class CachedCostItemWithSlots:
    """Slots implemented without __dict__."""

    __slots__ = "_cost"

    def __init__(self):
        self._cost = 1

    @cached_property
    def cost(self):
        """The cost of the item."""
        raise RuntimeError("never called, slots not supported")


# noinspection PyStatementEffect
@unittest.skipIf(sys.version_info >= (3, 8), "Python 3.8+ uses standard library implementation.")
class TestCachedProperty(unittest.TestCase):
    def test_cached(self):
        item = CachedCostItem()
        self.assertEqual(item.cost, 2)
        self.assertEqual(item.cost, 2)  # not 3

    def test_cached_attribute_name_differs_from_func_name(self):
        item = OptionallyCachedCostItem()
        self.assertEqual(item.get_cost(), 2)
        self.assertEqual(item.cached_cost, 3)
        self.assertEqual(item.get_cost(), 4)
        self.assertEqual(item.cached_cost, 3)

    def test_threaded(self):
        go = threading.Event()
        item = CachedCostItemWait(go)

        num_threads = 3

        orig_si = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            tpr = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads, thread_name_prefix="test")
            futures = [tpr.submit(lambda: item.cost) for _ in range(num_threads)]
            _, not_done = concurrent.futures.wait(futures)
            self.assertEqual(0, len(not_done), "Threads not stopped")
        finally:
            sys.setswitchinterval(orig_si)

        self.assertEqual(item.cost, 2)

    def test_object_with_slots(self):
        item = CachedCostItemWithSlots()
        with self.assertRaisesRegex(
            TypeError, "No '__dict__' attribute on 'CachedCostItemWithSlots' instance to cache 'cost' property.",
        ):
            item.cost

    def test_immutable_dict(self):
        class MyMeta(type):
            """Test metaclass."""
            @cached_property
            def prop(self):
                """Property impossible to cache standard way."""
                return True

        class MyClass(metaclass=MyMeta):
            """Test class."""
            pass

        with self.assertRaisesRegex(
            TypeError,
            "The '__dict__' attribute on 'MyMeta' instance "
            "does not support item assignment for caching 'prop' property.",
        ):
            MyClass.prop

    def test_reuse_different_names(self):
        """Disallow this case because decorated function a would not be cached."""
        with self.assertRaises(RuntimeError) as ctx:

            # noinspection PyUnusedLocal
            class ReusedCachedProperty:  # NOSONAR
                """Test class."""
                # noinspection PyPropertyDefinition
                @cached_property
                def a(self):  # NOSONAR
                    """Test getter."""
                    pass

                b = a

        self.assertEqual(
            str(ctx.exception.__context__),
            str(TypeError("Cannot assign the same cached_property to two different names ('a' and 'b').")),
        )

    def test_reuse_same_name(self):
        """Reusing a cached_property on different classes under the same name is OK."""
        counter = 0

        @cached_property
        def _cp(_self):
            nonlocal counter
            counter += 1
            return counter

        class A:  # NOSONAR
            """Test class 1."""
            cp = _cp

        class B:  # NOSONAR
            """Test class 2."""
            cp = _cp

        a = A()
        b = B()

        self.assertEqual(a.cp, 1)
        self.assertEqual(b.cp, 2)
        self.assertEqual(a.cp, 1)

    def test_set_name_not_called(self):
        cp = cached_property(lambda s: None)

        class Foo:
            """Test class."""
            pass

        Foo.cp = cp

        with self.assertRaisesRegex(
            TypeError, "Cannot use cached_property instance without calling __set_name__ on it.",
        ):
            # noinspection PyStatementEffect,PyUnresolvedReferences
            Foo().cp

    def test_access_from_class(self):
        self.assertIsInstance(CachedCostItem.cost, cached_property)

    def test_doc(self):
        self.assertEqual(CachedCostItem.cost.__doc__, "The cost of the item.")


@unittest.skipUnless(sys.version_info >= (3, 8), "Validate, that python 3.8 uses standard implementation")
class TestPy38Plus(unittest.TestCase):
    def test_is(self):
        import functools

        self.assertIs(cached_property, functools.cached_property, "Python 3.8+ should use standard implementation.")
