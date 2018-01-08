#!/usr/bin/env python


import confu
parser = confu.standard_parser("c-style log configuration script")
parser.add_argument("--log", dest="log_level",
    choices=("none", "error", "warning", "info", "debug"), default="debug")


def main(args):
    options = parser.parse_args(args)
    build = confu.Build.from_options(options)

    log_level_num = {
        "none": 0,
        "error": 1,
        "warning": 2,
        "info": 3,
        "debug": 4
    }[options.log_level]
    macros = {"CPUINFO_LOG_LEVEL": log_level_num}

    build.export_cpath("include", ["clog.h"])

    with build.options(source_dir="src", macros=macros, extra_include_dirs="src"):
        build.static_library("clog", build.cc("clog.c"))

    with build.options(source_dir="test", deps={
            (build, build.deps.googletest): all,
            "log": build.target.is_android}):
        build.unittest("clog-test", build.cxx("clog.cc"))

    return build

if __name__ == "__main__":
    import sys
    main(sys.argv[1:]).generate()
