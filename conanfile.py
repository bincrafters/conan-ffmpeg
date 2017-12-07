#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob
import shutil


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

    def build_requirements(self):
        self.build_requires("yasm_installer/1.3.0@bincrafters/testing")
        if self.settings.os == 'Windows':
            self.build_requires("msys2_installer/20161025@bincrafters/stable")

    def run(self, command, output=True, cwd=None):
        if self.settings.compiler == 'Visual Studio':
            with tools.environment_append({'PATH': [self.deps_env_info['msys2_installer'].MSYS_BIN]}):
                bash = "%MSYS_BIN%\\bash"
                vcvars_command = tools.vcvars_command(self.settings)
                command = "{vcvars_command} && {bash} -c ^'{command}'".format(
                    vcvars_command=vcvars_command,
                    bash=bash,
                    command=command)

                super(FFMpegConan, self).run(command, output, cwd)
        else:
            super(FFMpegConan, self).run(command, output, cwd)

    def build(self):
        with tools.chdir('sources'):
            prefix = tools.unix_path(self.package_folder) if self.settings.os == 'Windows' else self.package_folder
            args = ['--prefix=%s' % prefix,
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
                args.append('--toolchain=msvc')
            if self.settings.arch == 'x86':
                args.append('--arch=x86')

            # TODO : options
            args.append('--disable-sdl2')
            args.append('--disable-zlib')
            args.append('--disable-bzlib')
            args.append('--disable-lzma')
            args.append('--disable-iconv')

            env_build = AutoToolsBuildEnvironment(self)
            # ffmpeg's configure is not actually from autotools, so it doesn't understand standard options like
            # --host, --build, --target
            env_build.configure(args=args, build=False, host=False, target=False)
            env_build.make()
            env_build.make(args=['install'])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            # ffmpeg produces .a files which are actually .lib files
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                libs = glob.glob('*.a')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.lib')

    def package_info(self):
        libs = ['avdevice', 'avfilter', 'avformat', 'avcodec', 'swresample', 'swscale', 'avutil']
        if self.settings.compiler == 'Visual Studio':
            if self.options.shared:
                self.cpp_info.libs = libs
                self.cpp_info.libdirs.append('bin')
            else:
                self.cpp_info.libs = ['lib' + lib for lib in libs]
        else:
            self.cpp_info.libs = libs
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
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32'])
