import pytest
import json


@pytest.mark.test_extensions_import_module1
def test_extensions_import_module1(parse):

    # import sys
    # import importlib

    # from pathlib import Path

    extensions = parse("extensions")
    assert extensions.success, extensions.message

    sys_import = extensions.imports("sys")
    assert sys_import, "Are you importing `sys`?"

    importlib_import = extensions.imports("importlib")
    assert importlib_import, "Are you importing `importlib`?"

    path_import = extensions.from_imports("pathlib", "Path")
    assert path_import, "Are you importing `Path` from `pathlib`?"


@pytest.mark.test_extensions_sys_path_module1
def test_extensions_sys_path_module1(parse):

    # def load_module(directory, name):
    #     sys.path.insert(0, directory)

    extensions = parse("extensions")
    assert extensions.success, extensions.message

    load_module = extensions.defines("load_module")
    load_module_exists = load_module.exists()

    assert load_module_exists, "Are you defining a function called `load_module`?"

    load_module.has_arg("directory")
    arguments_exist = load_module.has_arg("directory") and load_module.has_arg(
        "name", 1
    )
    assert (
        arguments_exist
    ), "Does the `load_module` function have the correct arguments?"

    insert_call_exists = (
        load_module.calls()
        .match(
            {
                "value_func_value_value_id": "sys",
                "value_func_value_attr": "path",
                "value_func_attr": "insert",
                "value_args_0_value": 0,
                "value_args_1_id": "directory",
            }
        )
        .exists()
    )

    assert (
        insert_call_exists
    ), "Are you calling `sys.path.insert` and passing the correct parameters?"


@pytest.mark.test_extensions_import_pop_module1
def test_extensions_import_pop_module1(parse):

    #     importlib.import_module(name)
    #     sys.path.pop(0)

    extensions = parse("extensions")
    assert extensions.success, extensions.message

    load_module = extensions.defines("load_module")
    load_module_exists = load_module.exists()

    assert load_module_exists, "Are you defining a function called `load_module`?"

    import_module_call_exists = (
        load_module.calls()
        .match(
            {
                "value_func_value_id": "importlib",
                "value_func_attr": "import_module",
                "value_args_0_id": "name",
            }
        )
        .exists()
    )

    assert (
        import_module_call_exists
    ), "Are you calling `importlib.import_module` and passing the correct parameters?"

    pop_call_exists = (
        load_module.calls()
        .match(
            {
                "value_func_value_value_id": "sys",
                "value_func_value_attr": "path",
                "value_func_attr": "pop",
                "value_args_0_value": 0,
            }
        )
        .exists()
    )

    assert (
        pop_call_exists
    ), "Are you calling `sys.path.pop` and passing the correct parameters?"


@pytest.mark.test_extensions_load_directory_module1
def test_extensions_load_directory_module1(parse):

    # def load_directory(directory):
    #     for path in directory.rglob("*.py"):
    #         load_module(directory.as_posix(), path.stem)

    extensions = parse("extensions")
    assert extensions.success, extensions.message

    load_directory = extensions.defines("load_directory")
    load_directory_exists = load_directory.exists()

    assert load_directory_exists, "Are you defining a function called `load_directory`?"

    arguments_exist = load_directory.has_arg("directory")
    assert (
        arguments_exist
    ), "Does the `load_directory` function have the correct arguments?"

    for_exists = (
        load_directory.for_()
        .match(
            {
                "target_id": "path",
                "iter_type": "Call",
                "iter_func_value_id": "directory",
                "iter_func_attr": "rglob",
                "iter_args_0_value": "*.py",
            }
        )
        .exists()
    )

    assert (
        for_exists
    ), "Do you have a `for` loop that uses `rglob` to loop through `.py` files in `directory`?"

    load_module_call_exists = (
        load_directory.for_()
        .match(
            {
                "0_value_type": "Call",
                "0_value_func_id": "load_module",
                "0_value_args_0_type": "Call",
                "0_value_args_0_func_value_id": "directory",
                "0_value_args_0_func_attr": "as_posix",
                "0_value_args_1_value_id": "path",
                "0_value_args_1_attr": "stem",
            }
        )
        .exists()
    )

    assert (
        load_module_call_exists
    ), "Are you calling `load_module` and passing the correct parameters?"


@pytest.mark.test_extensions_load_bundled_module1
def test_extensions_load_bundled_module1(parse):

    # def load_bundled():
    #     directory = Path(__file__).parent / "extensions"
    #     load_directory(directory)

    extensions = parse("extensions")
    assert extensions.success, extensions.message

    load_bundled = extensions.defines("load_bundled")
    load_bundled_exists = load_bundled.exists()

    assert load_bundled_exists, "Are you defining a function called `load_bundled`?"

    load_bundled_assign_exists = load_bundled.assign_to().match(
        {
            "targets_0_id": "directory",
            "value_type": "BinOp",
            "value_left_value_type": "Call",
            "value_left_value_func_id": "Path",
            "value_left_value_args_0_id": "__file__",
            "value_left_attr": "parent",
            "value_op_type": "Div",
            "value_right_type": "Constant",
            "value_right_value": "extensions",
        }
    )

    assert (
        load_bundled_assign_exists
    ), "Are you calling `load_directory` and passing the correct parameters?"

    load_bundled_call_exists = (
        load_bundled.calls()
        .match({"value_func_id": "load_directory", "value_args_0_id": "directory"})
        .exists()
    )

    assert (
        load_bundled_call_exists
    ), "Are you calling `load_directory` and passing the correct parameters?"


@pytest.mark.test_site_load_bundled_module1
def test_site_load_bundled_module1(parse):

    # from ssg import extensions
    # extensions.load_bundled()

    site = parse("site")
    assert site.success, site.message

    extensions_import = site.from_imports("ssg", "extensions")
    assert extensions_import, "Are you importing `extensions` from `ssg`?"

    build = site.method("build")

    load_bundled_call_exists = (
        build.calls()
        .match(
            {
                "type": "Expr",
                "value_type": "Call",
                "value_func_value_id": "extensions",
                "value_func_attr": "load_bundled",
            }
        )
        .exists()
    )

    assert (
        load_bundled_call_exists
    ), "Are you calling `extensions.load_bundled()` in the `build` method?"
