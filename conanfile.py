#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class FFMpegConan(ConanFile):
    name = "ffmpeg"
    version = "3.4"
    url = "https://github.com/bincrafters/conan-ffmpeg"
    description = "A complete, cross-platform solution to record, convert and stream audio and video"
    license = "https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        with tools.chdir('sources'):
            args = ['--prefix=%s' % self.package_folder,
                    '--disable-doc',
                    '--disable-programs',
                    '--enable-pic']
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static', '--pkg-config-flags=--static'])
            if self.settings.build_type == 'Debug':
                args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug'])
            if self.settings.compiler == 'Visual Studio':
                args.append(' --toolchain=msvc')

            # TODO : options
            args.append('--disable-sdl2')
            args.append('--disable-zlib')
            args.append('--disable-bzlib')
            args.append('--disable-lzma')
            args.append('--disable-iconv')

            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=args)
            env_build.make()
            env_build.make(args=['install'])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework AppKit")
            self.cpp_info.exelinkflags.append("-framework AudioToolbox")
            self.cpp_info.exelinkflags.append("-framework VideoToolbox")
            self.cpp_info.exelinkflags.append("-framework CoreVideo")
            self.cpp_info.exelinkflags.append("-framework CoreMedia")
            self.cpp_info.exelinkflags.append("-framework CoreImage")
            self.cpp_info.exelinkflags.append("-framework CoreGraphics")
            self.cpp_info.exelinkflags.append("-framework CoreFoundation")
            self.cpp_info.exelinkflags.append("-framework OpenGL")
            self.cpp_info.exelinkflags.append("-framework Foundation")
            self.cpp_info.exelinkflags.append("-framework AVFoundation")
            self.cpp_info.exelinkflags.append("-framework Security")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
