import typing 


def strict(func) -> typing.Callable:
    def wrapper(*args, **kwargs):
        if not func.__annotations__:
            return func(*args, **kwargs)

        check = [*args][1::]
        
        if kwargs:
            check = check + list(kwargs.values())
            
        types = list(func.__annotations__.values())

        for i, arg in enumerate(check):
            if not isinstance(arg, types[i]):
                raise TypeError(f"{arg} value has incorrect type: {type(arg)}. It has to be: {types[i]}")

        return func(*args, **kwargs)

    return wrapper


def validate_id(id: int, dataset: typing.Dict) -> None:
    if id < 0:
        raise ValueError("Id must be a positive interger")
    
    if id not in dataset:
        raise IndexError("Provided id does not exist")
