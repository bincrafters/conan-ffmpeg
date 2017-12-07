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
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "zlib": [True, False],
               "bzlib": [True, False],
               "lzma": [True, False],
               "iconv": [True, False],
               "freetype": [True, False],
               "openjpeg": [True, False]}
    default_options = ("shared=False",
                       "fPIC=True",
                       "zlib=True",
                       "bzlib=True",
                       "lzma=True",
                       "iconv=True",
                       "freetype=True",
                       "openjpeg=True")

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build_requirements(self):
        self.build_requires("yasm_installer/1.3.0@bincrafters/testing")
        if self.settings.os == 'Windows':
            self.build_requires("msys2_installer/20161025@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/1.0.6@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/5.2.3@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/2.8.1@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/2.3.0@bincrafters/stable")

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
                    '--disable-programs']
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

            args.append('--enable-pic' if self.options.fPIC else '--disable-pic')
            args.append('--enable-zlib' if self.options.zlib else '--disable-zlib')
            args.append('--enable-bzlib' if self.options.bzlib else '--disable-bzlib')
            args.append('--enable-lzma' if self.options.lzma else '--disable-lzma')
            args.append('--enable-iconv' if self.options.iconv else '--disable-iconv')
            args.append('--enable-libfreetype' if self.options.freetype else '--disable-libfreetype')
            args.append('--enable-libopenjpeg' if self.options.openjpeg else '--disable-libopenjpeg')

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
            frameworks = ['AppKit', 'AudioToolbox', 'VideoToolbox', 'CoreVideo', 'CoreMedia', 'CoreImage',
                          'CoreGraphics', 'CoreFoundation', 'OpenGL', 'Foundation', 'AVFoundation', 'Security']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32'])
