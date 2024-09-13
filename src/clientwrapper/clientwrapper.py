from argparse import ArgumentParser, Namespace
from inspect import ismethod, signature
from typing import List, Optional, Any

from clientwrapper.utils import validate_unknown_args, parse_list


class ClientWrapper:
    """
    Allows access to  client functions via dictionary syntax agnostic of class

    Example:
    class YourClient(ClientWrapper):
        ...
    client = YourClient()
    token = client["functionName"](**kwargs)
    """
    all_funcs = None

    def __init__(self):
        """
        __init__ method to create the parser object and add subparsers for each function in the class
        Each function and its arguments are defined in this step
        self.all_funcs: list of all functions in the class
        """
        super().__init__()
        self.namespace = Namespace()
        self.parser = ArgumentParser(description=__name__)
        self.all_functions = [func for func in dir(self) if (not func.startswith("_"))]
        subparsers = self.parser.add_subparsers(dest="func")
        function_dict = {
            funcName: getattr(self, funcName) for funcName in self.all_functions if
            ismethod(getattr(self, funcName))
        }
        for funcName, func in function_dict.items():
            subParser = subparsers.add_parser(funcName)
            subParser.set_defaults(func=func)
            function_arguments = signature(func)
            for parameter in function_arguments.parameters:
                subParser.add_argument('--' + parameter, type=str, help='Argument for ' + funcName)

    def run(self, args: Optional[List[str]] = None) -> Any:
        """
        Parses the args and runs the function specified in the CLI func
        ClientWrapper creates a new instance of your class and runs the function specified in the CLI
        Instead of running multiple functions that set self.etc variables, run a single function that sets all values
        See docs/readme
        :param args: CLI args; can be provided as list for testing purposes (e.g. ['functionName', '--arg1', 'value1'])
        """
        validArgs = dict()
        knownArgsNamespace, unknownArgsList = self.parser.parse_known_args(args)
        defined_args = vars(knownArgsNamespace)
        for key in defined_args:
            if key == 'func':
                pass
            else:
                defined_args[key] = parse_list(defined_args[key])
        validArgs.update(defined_args)
        if len(unknownArgsList) > 0:
            unknownArgsListWithValidatedArgs = validate_unknown_args(unknownArgsList)
            validArgs.update(unknownArgsListWithValidatedArgs)
        setattr(self.namespace, 'func', getattr(knownArgsNamespace, "func"))
        knownArgsNamespace = vars(knownArgsNamespace)
        knownArgsNamespace.update(validArgs)
        knownArgsNamespace.pop('func', None)
        knownArgsNamespace.pop('kwargs', None)
        return self.namespace.func(**knownArgsNamespace)
