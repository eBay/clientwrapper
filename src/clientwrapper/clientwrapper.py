from argparse import ArgumentParser, Namespace
from inspect import ismethod, signature
import ast


class ClientWrapper():
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

    def _remove_extra_quotes_(self, string):
        if string.startswith("'"):
            string = string[1:]
        if string.endswith("'"):
            string = string[:-1]
        return string.strip()

    def _check_if_not_string_(self, string):
        """
        Checks if the string is a number or boolean
        :param string:
        :return: correctly typed obj
        """
        if string.isdigit():
            return int(string)
        elif string in ["True", "False"]:
            return bool(string)
        return string

    def _check_iterable_for_ints_(self, iterable):
        """
        Checks if all items in an iterable are ints or floats
        :param iterable:
        :return: correctly typed iterable
        """
        iterable_type = tuple if isinstance(iterable, tuple) else list if isinstance(iterable, list) else set
        iterable = list(map(self._remove_extra_quotes_, iterable))
        all_items_digits = all([item.isdigit() for item in iterable])
        if all_items_digits:
            any_items_floats = any([item.count(".") == 1 for item in iterable])
            if any_items_floats:
                return iterable_type([float(item) for item in iterable])
            return iterable_type([int(item) for item in iterable])
        return iterable

    def _parse_list_(self, string):
        """
        Parses a string that may be a list
        :string possible_list: str - string that may be a list
        :return: list or str
        """
        if string is None:
            return None
        try:
            return ast.literal_eval(string)
        except Exception:
            is_string = isinstance(string, str) and len(string) > 0
            if is_string:
                string = self._remove_extra_quotes_(string)
                string_is_list = string.startswith("[") and string.endswith("]")
                if string_is_list:
                    list_of_strings = string.strip('][').split(',')
                    return self._check_iterable_for_ints_(list_of_strings)
                string_is_tuple = string.startswith("(") and string.endswith(")")
                if string_is_tuple:
                    tuple_of_strings = tuple(string.strip('()').split(','))
                    return self._check_iterable_for_ints_(tuple_of_strings)
                string_is_dict_or_set = string.startswith("{") and string.endswith("}")
                if string_is_dict_or_set:
                    string_is_dict = ":" in string
                    if string_is_dict:
                        new_dict = dict()
                        for item in string.strip('{}').split(','):
                            formatted_key = self._remove_extra_quotes_(item.split(":")[0])
                            key = self._check_if_not_string_(formatted_key)
                            formatted_value = self._remove_extra_quotes_(item.split(":")[1])
                            value = self._check_if_not_string_(formatted_value)
                            new_dict[key] = value
                        return new_dict
                    return set(string.strip('{}').split(','))
            return self._check_if_not_string_(string)

    def run(self, args=None):
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
            if key=='func':
                pass
            else:
                defined_args[key] = self._parse_list_(defined_args[key])
        validArgs.update(defined_args)
        if len(unknownArgsList) > 0:
            unknownArgsListWithValidatedArgs = self._validate_unknown_args_(unknownArgsList)
            validArgs.update(unknownArgsListWithValidatedArgs)
        setattr(self.namespace, 'func', getattr(knownArgsNamespace, "func"))
        knownArgsNamespace = vars(knownArgsNamespace)
        knownArgsNamespace.update(validArgs)
        knownArgsNamespace.pop('func', None)
        knownArgsNamespace.pop('kwargs', None)
        return self.namespace.func(**knownArgsNamespace)

    def _validate_unknown_args_(self, args):
        """
        Validates the list args
        :param args:
        :return:
        """
        validArgs = dict()
        index = 0
        while index < len(args) - 1:
            arg_name = args[index].replace("--", "")
            arg_value = args[index + 1]
            value = self._parse_list_(arg_value)
            validArgs[arg_name] = value
            index += 2
        return validArgs
