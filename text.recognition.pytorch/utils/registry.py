class Registry(object):
    """Registry Class to map modules.

    The registry that provides name -> object mapping, to support third-party users' custom modules.

    To create a registry (inside detectron2):

    .. code-block:: python

        BACKBONE_REGISTRY = Registry('BACKBONE')

    To register an object:

    .. code-block:: python

        @BACKBONE_REGISTRY.register()
        class MyBackbone():
            ...

    Or:

    .. code-block:: python

        BACKBONE_REGISTRY.register(MyBackbone)
    """

    def __init__(self, name):
        """Init function.

        Args:
            name (str): the name of this registry
        """
        self._name = name

        self._obj_map = {}

    def _do_register(self, name, obj):
        upper_name = name.upper()
        assert (
            upper_name not in self._obj_map
        ), "An object named '{}' was already registered in '{}' registry!".format(upper_name, self._name)
        self._obj_map[upper_name] = obj

    def register(self, module_name=None, obj=None):
        """Register the given object under the the name `obj.__name__`.

        Can be used as either a decorator or not. See docstring of this class for usage.

        Args:
            module_name (str, optional): name of module. Defaults to None.
            obj (obj, optional): the object to register. Defaults to None.
        """
        if obj is None:
            # used as a decorator
            def deco(func_or_class):
                name = module_name if module_name is not None else func_or_class.__name__
                self._do_register(name, func_or_class)
                return func_or_class

            return deco

        # used as a function call
        name = module_name if module_name is not None else obj.__name__
        self._do_register(name, obj)

    def get(self, name):
        """Get object with name.

        Args:
            name (str): registered object name.

        Returns:
            obj: The object.
        """
        ret = self._obj_map.get(name.upper())
        if ret is None:
            raise KeyError("No object named '{}' found in '{}' registry[{}]!".format(
                name.upper(), self._name, self._obj_map.keys()))
        return ret

    def __getitem__(self, name):
        """Get object with name.

        Args:
            name (str): registered object name.

        Returns:
            obj: The object.
        """
        return self.get(name)

    def __str__(self):
        """Format to string representation."""
        s = self._name + ':'
        s += str(self._obj_map)
        return s
