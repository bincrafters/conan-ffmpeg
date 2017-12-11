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
               "openjpeg": [True, False],
               "opus": [True, False],
               "vorbis": [True, False],
               "zmq": [True, False],
               "alsa": [True, False],
               "jack": [True, False],
               "pulse": [True, False],
               "vaapi": [True, False],
               "vdpau": [True, False],
               "xcb": [True, False],
               "appkit": [True, False],
               "avfoundation": [True, False],
               "coreimage": [True, False],
               "audiotoolbox": [True, False],
               "videotoolbox": [True, False],
               "vda": [True, False],
               "securetransport": [True, False]}
    default_options = ("shared=False",
                       "fPIC=True",
                       "zlib=True",
                       "bzlib=True",
                       "lzma=True",
                       "iconv=True",
                       "freetype=False",  # TODO : freetype on Linux via pkg-config!
                       "openjpeg=True",
                       "opus=True",
                       "vorbis=True",
                       "zmq=True",
                       "alsa=True",
                       "jack=True",
                       "pulse=True",
                       "vaapi=True",
                       "vdpau=True",
                       "xcb=True",
                       "appkit=True",
                       "avfoundation=True",
                       "coreimage=True",
                       "audiotoolbox=True",
                       "videotoolbox=True",
                       "vda=False",
                       "securetransport=True")

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.remove("vaapi")
            self.options.remove("vdpau")
            self.options.remove("xcb")
            self.options.remove("alsa")
            self.options.remove("jack")
            self.options.remove("pulse")
        if self.settings.os != "Macos":
            self.options.remove("appkit")
            self.options.remove("avfoundation")
            self.options.remove("coreimage")
            self.options.remove("audiotoolbox")
            self.options.remove("videotoolbox")
            self.options.remove("vda")
            self.options.remove("securetransport")

    def build_requirements(self):
        self.build_requires("yasm_installer/[>=1.3.0]@bincrafters/stable")
        if self.settings.os == 'Windows':
            self.build_requires("msys2_installer/[>=20161025]@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/[>=1.2.11]@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/[>=1.0.6]@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/[>=5.2.3]@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/[>=1.15]@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/[>=2.8.1]@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/[>=2.3.0]@bincrafters/stable")
        if self.options.vorbis:
            self.requires.add("vorbis/[>=1.3.5]@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/[>=1.2.1]@bincrafters/stable")
        if self.options.zmq:
            self.requires.add("zmq/[>=4.2.2]@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                arch_suffix = ''
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    arch_suffix = ':i386'

                packages = ['pkg-config']
                if self.options.alsa:
                    packages.append('libasound2-dev%s' % arch_suffix)
                if self.options.jack:
                    packages.append('libjack-dev%s' % arch_suffix)
                if self.options.pulse:
                    packages.append('libpulse-dev%s' % arch_suffix)
                if self.options.vaapi:
                    packages.append('libva-dev%s' % arch_suffix)
                if self.options.vdpau:
                    packages.append('libvdpau-dev%s' % arch_suffix)
                if self.options.xcb:
                    packages.extend(['libxcb1-dev%s' % arch_suffix,
                                     'libxcb-shm0-dev%s' % arch_suffix,
                                     'libxcb-shape0-dev%s' % arch_suffix,
                                     'libxcb-xfixes0-dev%s' % arch_suffix])
                for package in packages:
                    installer.install(package)

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

    def copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        for pc_name in pc_files:
            new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            tools.replace_prefix_in_pc_file(new_pc, root)

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
            args.append('--enable-libvorbis' if self.options.vorbis else '--disable-libvorbis')
            args.append('--enable-libopus' if self.options.opus else '--disable-libopus')
            args.append('--enable-libzmq' if self.options.zmq else '--disable-libzmq')

            if self.settings.os == "Linux":
                args.append('--enable-alsa' if self.options.alsa else '--disable-alsa')
                args.append('--enable-jack' if self.options.jack else '--disable-jack')
                args.append('--enable-libpulse' if self.options.pulse else '--disable-libpulse')
                args.append('--enable-vaapi' if self.options.vaapi else '--disable-vaapi')
                args.append('--enable-vdpau' if self.options.vdpau else '--disable-vdpau')
                if self.options.xcb:
                    args.extend(['--enable-libxcb', '--enable-libxcb-shm',
                                 '--enable-libxcb-shape', '--enable-libxcb-xfixes'])
                else:
                    args.extend(['--disable-libxcb', '--disable-libxcb-shm',
                                 '--disable-libxcb-shape', '--disable-libxcb-xfixes'])

            if self.settings.os == "Macos":
                args.append('--enable-appkit' if self.options.appkit else '--disable-appkit')
                args.append('--enable-avfoundation' if self.options.avfoundation else '--disable-avfoundation')
                args.append('--enable-coreimage' if self.options.avfoundation else '--disable-coreimage')
                args.append('--enable-audiotoolbox' if self.options.audiotoolbox else '--disable-audiotoolbox')
                args.append('--enable-videotoolbox' if self.options.videotoolbox else '--disable-videotoolbox')
                args.append('--enable-vda' if self.options.vda else '--disable-vda')
                args.append('--enable-securetransport' if self.options.securetransport else '--disable-securetransport')

            os.makedirs('pkgconfig')
            if self.options.opus:
                self.copy_pkg_config('opus')
            if self.options.vorbis:
                self.copy_pkg_config('ogg')
                self.copy_pkg_config('vorbis')
            if self.options.zmq:
                self.copy_pkg_config('zmq')

            env_vars = {'PKG_CONFIG_PATH': os.path.abspath('pkgconfig')}

            with tools.environment_append(env_vars):
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
            frameworks = ['CoreVideo', 'CoreMedia', 'CoreGraphics', 'CoreFoundation', 'OpenGL', 'Foundation']
            if self.options.appkit:
                frameworks.append('AppKit')
            if self.options.avfoundation:
                frameworks.append('AVFoundation')
            if self.options.coreimage:
                frameworks.append('CoreImage')
            if self.options.audiotoolbox:
                frameworks.append('AudioToolbox')
            if self.options.videotoolbox:
                frameworks.append('VideoToolbox')
            if self.options.vda:
                frameworks.append('VideoDecodeAcceleration')
            if self.options.securetransport:
                frameworks.append('Security')
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
            if self.options.alsa:
                self.cpp_info.libs.append('asound')
            if self.options.jack:
                self.cpp_info.libs.append('jack')
            if self.options.pulse:
                self.cpp_info.libs.append('pulse')
            if self.options.vaapi:
                self.cpp_info.libs.extend(['va', 'va-drm', 'va-x11'])
            if self.options.vdpau:
                self.cpp_info.libs.extend(['vdpau', 'X11'])
            if self.options.xcb:
                self.cpp_info.libs.extend(['xcb', 'xcb-shm', 'xcb-shape', 'xcb-xfixes'])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32'])
