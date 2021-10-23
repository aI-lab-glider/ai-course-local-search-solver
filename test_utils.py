from copy import deepcopy
import importlib
import inspect
import os
import pathlib
import sys
from contextlib import contextmanager
from os.path import isfile
from functools import partial, wraps
from types import ModuleType
from typing import Generic, TypeVar, Union
import pytest

ALLOWED_EXCEPTIONS = [
    "ValueError", "IndexError", "AttributeError", "KeyError", "RecursionError", "OverflowError", "SyntaxError",
    "TypeError", "ZeroDivisionError", "IndentationError", "NotImplementedError"
]

BOBOT_FILES = ["test_utils.py", "grading.py"]

hide_exceptions = True


class BobotError(Exception):
    original: Exception


def wrap_class(base):
    class ClassWrapper(base):
        def __getattribute__(self, name):
            original = base.__getattribute__(self, name)

            def func_wrapper(*args, **kwargs):
                with intercept_exceptions():
                    return original(*args, **kwargs)

            return func_wrapper

    return ClassWrapper


@contextmanager
def intercept_exceptions():
    global hide_exceptions
    if hide_exceptions:
        try:
            yield
        except BobotError:
            raise BobotError("Tested code raises RecursionError.") from None
        except BaseException as e:
            if str(e).startswith("Timeout"):
                raise BobotError("Test timeout") from None

            print(f"wtf {e.__class__.__name__}")
            _, _, exc_tb = sys.exc_info()

            # hit bottom of the stack trace or go beyond strict project files
            while exc_tb.tb_next is not None and isfile(exc_tb.tb_next.tb_frame.f_code.co_filename):
                exc_tb = exc_tb.tb_next

            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            file_line_no = exc_tb.tb_lineno
            error_location_msg = f" in {file_name}:{file_line_no}" if file_name not in BOBOT_FILES else ""
            error = BobotError(
                f"Tested code raises {print_exception_type(e)}{error_location_msg}")
            error.original = e
            raise error from None
    else:
        yield


def print_exception_type(e):
    if e.__class__.__name__ in ALLOWED_EXCEPTIONS:
        return e.__class__.__name__
    else:
        return "UnknownException"


@contextmanager
def intercept_local_exceptions(message):
    if hide_exceptions:
        failed = False
        try:
            yield
        except:
            failed = True

        if failed:
            pytest.fail(message)
    else:
        yield


class SafeModule:
    def __init__(self, module):
        self.module = module

    def __getattr__(self, att_name):

        if inspect.isclass(getattr(self.module, att_name)):
            SafeClass = wrap_class(getattr(self.module, att_name))
            return SafeClass

        elif inspect.isfunction(getattr(self.module, att_name)):

            def function(*args, **kwargs):
                with intercept_exceptions():
                    return getattr(self.module, att_name)(*args, **kwargs)

            return function
        else:
            raise AttributeError(
                "accessing other Python structures than classes and functions is not allowed")


class RelativePathLoader:
    basedir: pathlib.Path

    def __init__(self, basedir_str: str) -> None:
        self.basedir = pathlib.Path(basedir_str)

    def load(self, relative_path_str: Union[str, pathlib.Path]) -> object:
        relative_path = pathlib.Path(relative_path_str)
        name = ".".join(relative_path.with_suffix("").parts)
        full_path = self.basedir.joinpath(relative_path)

        spec = importlib.util.spec_from_file_location(name, full_path)
        module = importlib.util.module_from_spec(spec)

        with intercept_exceptions():
            spec.loader.exec_module(module)

        return module


T = TypeVar('T')


def create_object_copy_with_student_method(original: T,
                                           student_loader: RelativePathLoader,
                                           student_code_path: Union[pathlib.Path, str],
                                           method_name: str) -> T:
    """A function that transplants a method from the class implemented by student
    to a receiver (normally it would a correct class implemented by the teacher)  
    """
    receiver = deepcopy(original)
    students_module = student_loader.load(student_code_path)

    assert not inspect.isclass(receiver)
    receiver_cls = getattr(students_module, receiver.__class__.__name__)
    method = getattr(receiver_cls, method_name)

    @wraps(method)
    def safe_method(*args, **kwargs):
        with intercept_exceptions():
            return method(*args, **kwargs)

    safe_method = partial(safe_method, receiver)
    object.__setattr__(receiver, method_name, safe_method)
    return receiver


@contextmanager
def override_static_method(receiver: T,
                           student_loader: RelativePathLoader,
                           student_code_path: pathlib.Path,
                           method_name: str) -> T:
    students_module = student_loader.load(student_code_path)

    assert inspect.isclass(receiver)
    receiver_cls = getattr(students_module, receiver.__name__)
    method = getattr(receiver_cls, method_name)
    original_method = getattr(receiver, method_name)

    def safe_method(*args, **kwargs):
        with intercept_exceptions():
            return method(*args, **kwargs)

    safe_method = staticmethod(safe_method)
    setattr(receiver, method_name, safe_method)
    try:
        yield receiver
    finally:
        setattr(receiver, method_name, original_method)
