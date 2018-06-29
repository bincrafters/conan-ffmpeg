#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
from conans import tools
from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    if tools.os_info.is_linux and os.getenv("CONAN_GCC_VERSIONS") == 8:
        if not os.getenv("CONAN_BUILD_POLICY"):
            os.environ["CONAN_BUILD_POLICY"] = "missing"
        for shared_option in [False, True]:
            custom_options = {"ffmpeg:vdpau": False, "ffmpeg:vaapi": False, "ffmpeg:xcb": False, 'ffmpeg:shared': shared_option}
            builder.add({'arch': 'x86', 'build_type': 'Release', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)
            builder.add({'arch': 'x86', 'build_type': 'Debug', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)
            builder.add({'arch': 'x86_64', 'build_type': 'Release', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)
            builder.add({'arch': 'x86_64', 'build_type': 'Debug', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)

    builder.run()
