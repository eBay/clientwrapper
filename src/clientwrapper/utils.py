import ast
from typing import Union, List, Iterable, Optional


def remove_extra_single_quotes(string: str) -> str:
    if string.startswith("'"):
        string = string[1:]
    if string.endswith("'"):
        string = string[:-1]
    return string.strip()


def check_if_not_string(string: str) -> Union[str, int, float, bool]:
    """
    Checks if the string is a number or boolean
    :param string:
    :return: correctly typed obj
    """
    if string.isdigit():
        if "." in string:
            return float(string)
        return int(string)
    elif string in ["True", "False"]:
        return bool(string)
    return string


def check_iterable_for_ints(
        iterable: Iterable[Union[str, int, float, bool]]
) -> Iterable[Union[str, int, float, bool]]:
    """
    Checks if all items in an iterable are ints or floats
    :param iterable:
    :return: correctly typed iterable
    """
    iterable_type = tuple if isinstance(iterable, tuple) else list if isinstance(iterable, list) else set
    iterable = list(map(remove_extra_single_quotes, iterable))
    all_items_digits = all([item.isdigit() for item in iterable])
    if all_items_digits:
        any_items_floats = any([item.count(".") == 1 for item in iterable])
        if any_items_floats:
            return iterable_type([float(item) for item in iterable])
        return iterable_type([int(item) for item in iterable])
    return iterable


def parse_list(string: str) -> Optional[Iterable[Union[str, int, float, bool]]]:
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
            string = remove_extra_single_quotes(string)
            string_is_list = string.startswith("[") and string.endswith("]")
            if string_is_list:
                list_of_strings = string.strip('][').split(',')
                return check_iterable_for_ints(list_of_strings)
            string_is_tuple = string.startswith("(") and string.endswith(")")
            if string_is_tuple:
                tuple_of_strings = tuple(string.strip('()').split(','))
                return check_iterable_for_ints(tuple_of_strings)
            string_is_dict_or_set = string.startswith("{") and string.endswith("}")
            if string_is_dict_or_set:
                string_is_dict = ":" in string
                if string_is_dict:
                    new_dict = dict()
                    for item in string.strip('{}').split(','):
                        formatted_key = remove_extra_single_quotes(item.split(":")[0])
                        key = check_if_not_string(formatted_key)
                        formatted_value = remove_extra_single_quotes(item.split(":")[1])
                        value = check_if_not_string(formatted_value)
                        new_dict[key] = value
                    return new_dict
                return set(string.strip('{}').split(','))
        return check_if_not_string(string)


def validate_unknown_args(args: List[str]) -> dict:
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
        value = parse_list(arg_value)
        validArgs[arg_name] = value
        index += 2
    return validArgs
