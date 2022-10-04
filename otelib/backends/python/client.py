"""Client for python backend."""
from otelib.backends.python import (
    DataResource,
    Filter,
    Function,
    Mapping,
    Transformation,
)


# pylint: disable=duplicate-code
class OTEPythonClient:
    """The Python version of the OTEClient object.

    Parameters:
        Interpreter (str): Interpreter for the python backend.

    Attributes:
        Interpreter (str): Interpreter for the python backend.

    """

    def __init__(self, interpreter: str) -> None:
        """Initiates an OTEAPI Service client.

        The `interpreter` indicates which intepreter to use for the python backend
        currently only 'python' is supported
        """
        self.interpreter: str = interpreter
        if interpreter != "python":
            raise NotImplementedError(
                "Only python interpreter supported for python backend"
            )

    def create_dataresource(self, **kwargs) -> DataResource:
        """Create a new data resource.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created data resource.

        """
        data_resource = DataResource(self.interpreter)
        data_resource.create(**kwargs)
        return data_resource

    def create_transformation(self, **kwargs) -> Transformation:
        """Create a new transformation.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created transformation.

        """
        transformation = Transformation(self.interpreter)
        transformation.create(**kwargs)
        return transformation

    def create_filter(self, **kwargs) -> Filter:
        """Create a new filter.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created filter.

        """
        filter_ = Filter(self.interpreter)
        filter_.create(**kwargs)
        return filter_

    def create_mapping(self, **kwargs) -> Mapping:
        """Create a new mapping.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created mapping.

        """
        mapping = Mapping(self.interpreter)
        mapping.create(**kwargs)
        return mapping

    def create_function(self, **kwargs) -> Function:
        """Create a new function.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created function.

        """
        function_ = Function(self.interpreter)
        function_.create(**kwargs)
        return function_
