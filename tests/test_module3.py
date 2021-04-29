import pytest
import json


@pytest.mark.test_menu_imports_module3
def test_menu_imports_module3(parse):

    # from ssg import hooks, parsers

    # files = []

    menu = parse("menu")
    assert menu.success, menu.message

    hooks_import = menu.from_imports("ssg", "hooks")
    assert hooks_import, "Are you importing `hooks` from `ssg`?"

    parsers_import = menu.from_imports("ssg", "parsers")
    assert parsers_import, "Are you importing `parsers` from `ssg`?"

    files = (
        menu.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "files",
                "value_type": "List",
            }
        )
        .exists()
    )
    assert (
        files
    ), "Are you creating a variable called `files` set equal to an empty list?"


@pytest.mark.test_menu_collect_files_module3
def test_menu_collect_files_module3(parse):

    # @hooks.register("collect_files")
    # def collect_files(source, site_parsers):
    #     valid = lambda p: not isinstance(p, parsers.ResourceParser)

    menu = parse("menu")
    assert menu.success, menu.message

    collect_files = menu.query("def collect_files(source, site_parsers): ??")
    collect_files_exists = collect_files.exists()

    assert (
        collect_files_exists
    ), "Are you defining a function called `collect_files` with the correct arguments?"

    decorator = (
        collect_files.decorators()
        .match(
            {
                "0_type": "Call",
                "0_func_type": "Attribute",
                "0_func_value_type": "Name",
                "0_func_value_id": "hooks",
                "0_func_attr": "register",
                "0_args_0_type": "Constant",
                "0_args_0_value": "collect_files",
            }
        )
        .exists()
    )
    assert (
        decorator
    ), 'Has the `collect_files` function been decorated with `@hooks.register()` passing in `"collect_files"`?'

    valid = (
        collect_files.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_id": "valid",
                "value_type": "Lambda",
                "value_args_args_0_arg": "p",
                "value_body_type": "UnaryOp",
                "value_body_op_type": "Not",
                "value_body_operand_type": "Call",
                "value_body_operand_func_id": "isinstance",
                "value_body_operand_args_0_id": "p",
                "value_body_operand_args_1_value_id": "parsers",
                "value_body_operand_args_1_attr": "ResourceParser",
            }
        )
        .exists()
    )
    assert (
        valid
    ), "Are you creating a variable called `valid` set equal to a `lambda` that has an argument `p`? In the body are you testing if `p` is an instance of `parsers.ResourceParser`?"


@pytest.mark.test_menu_for_build_list_module3
def test_menu_for_build_list_module3(parse):

    #     for path in source.rglob("*"):
    #         for parser in list(filter(valid, site_parsers)):
    #             if parser.valid_file_ext(path.suffix):
    #                 files.append(path)

    menu = parse("menu")
    assert menu.success, menu.message

    collect_files = menu.query("def collect_files(source, site_parsers): ??")
    collect_files_exists = collect_files.exists()

    assert (
        collect_files_exists
    ), "Are you defining a function called `collect_files` with the correct arguments?"

    first_for_exists = (
        collect_files.for_()
        .match(
            {
                "target_type": "Name",
                "target_id": "path",
                "iter_type": "Call",
                "iter_func_type": "Attribute",
                "iter_func_value_type": "Name",
                "iter_func_value_id": "source",
                "iter_func_attr": "rglob",
                "iter_args_0_type": "Constant",
                "iter_args_0_value": "*",
            }
        )
        .exists()
    )

    assert (
        first_for_exists
    ), 'Do you have a `for` loop, looping through `source.rglob("*")`? Is the current loop value called `path`?'

    second_for_exists = (
        collect_files.for_()
        .match(
            {
                "0_type": "For",
                "0_target_type": "Name",
                "0_target_id": "parser",
                "0_iter_type": "Call",
                "0_iter_func_type": "Name",
                "0_iter_func_id": "list",
                "0_iter_args_0_type": "Call",
                "0_iter_args_0_func_type": "Name",
                "0_iter_args_0_func_id": "filter",
                "0_iter_args_0_args_0_type": "Name",
                "0_iter_args_0_args_0_id": "valid",
                "0_iter_args_0_args_1_type": "Name",
                "0_iter_args_0_args_1_id": "site_parsers",
            }
        )
        .exists()
    )

    assert (
        second_for_exists
    ), "Do you have a nested `for` loop,  looping through `list(filter(valid, site_parsers))`? Is the current loop value called `parser`?"

    if_exists = (
        collect_files.for_()
        .match(
            {
                "0_body_0_type": "If",
                "0_body_0_test_type": "Call",
                "0_body_0_test_func_type": "Attribute",
                "0_body_0_test_func_value_type": "Name",
                "0_body_0_test_func_value_id": "parser",
                "0_body_0_test_func_attr": "valid_file_ext",
                "0_body_0_test_args_0_type": "Attribute",
                "0_body_0_test_args_0_value_type": "Name",
                "0_body_0_test_args_0_value_id": "path",
                "0_body_0_test_args_0_attr": "suffix",
            }
        )
        .exists()
    )

    assert (
        if_exists
    ), "Are you testing if `path.suffix` is a valid file extension with `parser.valid_file_ext()`?"

    files_append_exists = (
        collect_files.for_()
        .match(
            {
                "0_body_0_body_0_type": "Expr",
                "0_body_0_body_0_value_type": "Call",
                "0_body_0_body_0_value_func_type": "Attribute",
                "0_body_0_body_0_value_func_value_type": "Name",
                "0_body_0_body_0_value_func_value_id": "files",
                "0_body_0_body_0_value_func_attr": "append",
                "0_body_0_body_0_value_args_0_type": "Name",
                "0_body_0_body_0_value_args_0_id": "path",
            }
        )
        .exists()
    )

    assert (
        files_append_exists
    ), "Are you testing if `path.suffix` is a valid file extension with `parser.valid_file_ext()`?"


@pytest.mark.test_menu_generate_menu_module3
def test_menu_generate_menu_module3(parse):

    # @hooks.register("generate_menu")
    # def generate_menu(html, ext):
    #     template = '<li><a href="{}{}">{}</a></li>'

    menu = parse("menu")
    assert menu.success, menu.message

    generate_menu = menu.query("def generate_menu(html, ext): ??")
    generate_menu_exists = generate_menu.exists()

    assert (
        generate_menu_exists
    ), "Are you defining a function called `generate_menu` with the correct arguments?"

    decorator = (
        generate_menu.decorators()
        .match(
            {
                "0_type": "Call",
                "0_func_type": "Attribute",
                "0_func_value_type": "Name",
                "0_func_value_id": "hooks",
                "0_func_attr": "register",
                "0_args_0_type": "Constant",
                "0_args_0_value": "generate_menu",
            }
        )
        .exists()
    )
    assert (
        decorator
    ), 'Has the `generate_menu` function been decorated with `@hooks.register()` passing in `"generate_menu"`?'

    template = (
        generate_menu.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "template",
                "value_type": "Constant",
                "value_value": '<li><a href="{}{}">{}</a></li>',
            }
        )
        .exists()
    )
    assert (
        template
    ), "Are you creating a variable called `template` and setting it equal to `'<li><a href=\"{}{}\">{}</a></li>'`?"


@pytest.mark.test_menu_lambda_module3
def test_menu_lambda_module3(parse):

    #     menu_item = lambda name, ext: template.format(name, ext, name.title())

    menu = parse("menu")
    assert menu.success, menu.message

    generate_menu = menu.query("def generate_menu(html, ext): ??")
    generate_menu_exists = generate_menu.exists()

    assert (
        generate_menu_exists
    ), "Are you defining a function called `generate_menu` with the correct arguments?"

    menu_item = (
        generate_menu.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "menu_item",
                "value_type": "Lambda",
                "value_args_type": "arguments",
                "value_args_args_0_type": "arg",
                "value_args_args_0_arg": "name",
                "value_args_args_1_type": "arg",
                "value_args_args_1_arg": "ext",
                "value_body_type": "Call",
                "value_body_func_type": "Attribute",
                "value_body_func_value_type": "Name",
                "value_body_func_value_id": "template",
                "value_body_func_attr": "format",
                "value_body_args_0_type": "Name",
                "value_body_args_0_id": "name",
                "value_body_args_1_type": "Name",
                "value_body_args_1_id": "ext",
                "value_body_args_2_type": "Call",
                "value_body_args_2_func_type": "Attribute",
                "value_body_args_2_func_value_type": "Name",
                "value_body_args_2_func_value_id": "name",
                "value_body_args_2_func_attr": "title",
            }
        )
        .exists()
    )

    assert (
        menu_item
    ), "Are you creating a variable called `menu_item` set equal to a `lambda` that has two arguments `name` and `ext`? In the body are you calling `format()` on `template`? Are you passing `name`, `ext`, and `name.title()` to `format()`?"


@pytest.mark.test_menu_names_module3
def test_menu_names_module3(parse):

    #     menu = "\n".join([menu_item(path.stem, ext) for path in files])

    menu = parse("menu")
    assert menu.success, menu.message

    generate_menu = menu.query("def generate_menu(html, ext): ??")
    generate_menu_exists = generate_menu.exists()

    assert (
        generate_menu_exists
    ), "Are you defining a function called `generate_menu` with the correct arguments?"

    menu_item = (
        generate_menu.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "menu",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Constant",
                "value_func_value_value": "\n",
                "value_func_attr": "join",
                "value_args_0_type": "ListComp",
                "value_args_0_elt_type": "Call",
                "value_args_0_elt_func_type": "Name",
                "value_args_0_elt_func_id": "menu_item",
                "value_args_0_elt_args_0_type": "Attribute",
                "value_args_0_elt_args_0_value_type": "Name",
                "value_args_0_elt_args_0_value_id": "path",
                "value_args_0_elt_args_0_attr": "stem",
                "value_args_0_elt_args_1_type": "Name",
                "value_args_0_elt_args_1_id": "ext",
                "value_args_0_generators_0_type": "comprehension",
                "value_args_0_generators_0_target_type": "Name",
                "value_args_0_generators_0_target_id": "path",
                "value_args_0_generators_0_iter_type": "Name",
                "value_args_0_generators_0_iter_id": "files",
                "value_args_0_generators_0_is_async": 0,
            }
        )
        .exists()
    )

    assert (
        menu_item
    ), 'Are you creating a variable called `menu` set equal to a call to `"\\n".join()`? Are you passing a list comprehension to `join()`? Do you have an iterator of `path in files`? As the result do you have a call to `menu_item()` passing in `path.stem` and `ext`?'


@pytest.mark.test_menu_list_template_module3
def test_menu_list_template_module3(parse):

    #     return "<ul>\n{}</ul>\n{}".format(menu, html)

    menu = parse("menu")
    assert menu.success, menu.message

    generate_menu = menu.query("def generate_menu(html, ext): ??")
    generate_menu_exists = generate_menu.exists()
    assert (
        generate_menu_exists
    ), "Are you defining a function called `generate_menu` with the correct arguments?"

    menu_item = (
        generate_menu.returns_call()
        .match(
            {
                "type": "Return",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Constant",
                "value_func_value_value": "<ul>\n{}</ul>\n{}",
                "value_func_attr": "format",
                "value_args_0_type": "Name",
                "value_args_0_id": "menu",
                "value_args_1_type": "Name",
                "value_args_1_id": "html",
            }
        )
        .exists()
    )
    assert (
        menu_item
    ), 'Are you returning the string `"<ul>\\n{}</ul>\\n{}"` with a call to `format()` appended. Are you passing `menu` and `html` to `format()`?'


@pytest.mark.test_site_collect_files_event_module3
def test_site_collect_files_event_module3(parse):

    # , hooks
    #        hooks.event("collect_files", self.source, self.parsers)

    site = parse("site")
    assert site.success, site.message

    hooks_import = site.from_imports("ssg", "hooks")
    assert hooks_import, "Are you importing `hooks` from `ssg`?"

    build = site.method("build")

    hooks_event_exists = (
        build.calls()
        .match(
            {
                "type": "Expr",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Name",
                "value_func_value_id": "hooks",
                "value_func_attr": "event",
                "value_args_0_type": "Constant",
                "value_args_0_value": "collect_files",
                "value_args_1_type": "Attribute",
                "value_args_1_value_type": "Name",
                "value_args_1_value_id": "self",
                "value_args_1_attr": "source",
                "value_args_2_type": "Attribute",
                "value_args_2_value_type": "Name",
                "value_args_2_value_id": "self",
                "value_args_2_attr": "parsers",
            }
        )
        .exists()
    )

    assert (
        hooks_event_exists
    ), 'Are you calling `hooks.event()` in the `build` method? And are you passing in `"collect_files"`, `self.source`,  and `self.parsers`?'


@pytest.mark.test_parsers_md_menu_filter_module3
def test_parsers_md_menu_filter_module3(parse):

    # from ssg import hook

    #        filtered = hooks.filter("generate_menu", html, self.base_ext)
    #        self.write(path, dest, filtered)

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    hooks_import = parsers.from_imports("ssg", "hooks")
    assert hooks_import, "Are you importing `hooks` from `ssg`?"

    markdown_parse = parsers.class_("MarkdownParser").defines("parse")

    hooks_filter_exists = (
        markdown_parse.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "filtered",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Name",
                "value_func_value_id": "hooks",
                "value_func_attr": "filter",
                "value_args_0_type": "Constant",
                "value_args_0_value": "generate_menu",
                "value_args_1_type": "Name",
                "value_args_1_id": "html",
                "value_args_2_type": "Attribute",
                "value_args_2_value_type": "Name",
                "value_args_2_value_id": "self",
                "value_args_2_attr": "base_ext",
            }
        )
        .exists()
    )

    assert (
        hooks_filter_exists
    ), 'Are you calling `hooks.filter()` and assigning it to a variable called `filtered`? And are you passing in `"generate_menu"`, `html`,  and `self.base_ext`?'

    self_write_exists = (
        markdown_parse.calls()
        .match(
            {
                "type": "Expr",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Name",
                "value_func_value_id": "self",
                "value_func_attr": "write",
                "value_args_0_type": "Name",
                "value_args_0_id": "path",
                "value_args_1_type": "Name",
                "value_args_1_id": "dest",
                "value_args_2_type": "Name",
                "value_args_2_id": "filtered",
            }
        )
        .exists()
    )

    assert (
        self_write_exists
    ), "Are you calling `self.write()` and passing in `path`, `dest`,  and `filtered`?"


@pytest.mark.test_parsers_rst_menu_filter_module3
def test_parsers_rst_menu_filter_module3(parse):

    #        filtered = hooks.filter("generate_menu", html["html_body"], self.base_ext)
    #        self.write(path, dest, filtered)

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    rst_parse = parsers.class_("ReStructuredTextParser").defines("parse")
    hooks_filter_exists = (
        rst_parse.assign_to()
        .match(
            {
                "type": "Assign",
                "targets_0_type": "Name",
                "targets_0_id": "filtered",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Name",
                "value_func_value_id": "hooks",
                "value_func_attr": "filter",
                "value_args_0_type": "Constant",
                "value_args_0_value": "generate_menu",
                "value_args_1_type": "Subscript",
                "value_args_1_value_type": "Name",
                "value_args_1_value_id": "html",
                "value_args_1_slice_type": "Index",
                "value_args_1_slice_value_type": "Constant",
                "value_args_1_slice_value_value": "html_body",
                "value_args_2_type": "Attribute",
                "value_args_2_value_type": "Name",
                "value_args_2_value_id": "self",
                "value_args_2_attr": "base_ext",
            }
        )
        .exists()
    )

    assert (
        hooks_filter_exists
    ), 'Are you calling `hooks.filter()` and assigning it to a variable called `filtered`? And are you passing in `"generate_menu"`, `html`,  and `self.base_ext`?'

    self_write_exists = (
        rst_parse.calls()
        .match(
            {
                "type": "Expr",
                "value_type": "Call",
                "value_func_type": "Attribute",
                "value_func_value_type": "Name",
                "value_func_value_id": "self",
                "value_func_attr": "write",
                "value_args_0_type": "Name",
                "value_args_0_id": "path",
                "value_args_1_type": "Name",
                "value_args_1_id": "dest",
                "value_args_2_type": "Name",
                "value_args_2_id": "filtered",
            }
        )
        .exists()
    )

    assert (
        self_write_exists
    ), "Are you calling `self.write()` and passing in `path`, `dest`,  and `filtered`?"
