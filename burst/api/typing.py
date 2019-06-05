from typing import Union, Any, List, Dict

# define a type for the returned stuff of parsed JSON,
# at least until the fine folks at https://github.com/python/typing/issues/182 find a solution.
JSONType = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
