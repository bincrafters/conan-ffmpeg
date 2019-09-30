#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os
import glob
import shutil


class FFMpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.2"
    url = "https://github.com/bincrafters/conan-ffmpeg"
    description = "A complete, cross-platform solution to record, convert and stream audio and video"
    # https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md
    license = "LGPL-2.1-or-later", "GPL-2.0-or-later"
    homepage = "https://ffmpeg.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = "ffmpeg", "multimedia", "audio", "video", "encoder", "decoder", "encoding", "decoding",\
             "transcoding", "multiplexer", "demultiplexer", "streaming"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "postproc": [True, False],
               "zlib": [True, False],
               "bzlib": [True, False],
               "lzma": [True, False],
               "iconv": [True, False],
               "freetype": [True, False],
               "openjpeg": [True, False],
               "openh264": [True, False],
               "opus": [True, False],
               "vorbis": [True, False],
               "zmq": [True, False],
               "sdl2": [True, False],
               "x264": [True, False],
               "x265": [True, False],
               "vpx": [True, False],
               "mp3lame": [True, False],
               "fdk_aac": [True, False],
               "webp": [True, False],
               "openssl": [True, False],
               "alsa": [True, False],
               "pulse": [True, False],
               "vaapi": [True, False],
               "vdpau": [True, False],
               "xcb": [True, False],
               "appkit": [True, False],
               "avfoundation": [True, False],
               "coreimage": [True, False],
               "audiotoolbox": [True, False],
               "videotoolbox": [True, False],
               "securetransport": [True, False],
               "qsv": [True, False]}
    default_options = {'shared': False,
                       'fPIC': True,
                       'postproc': True,
                       'zlib': True,
                       'bzlib': True,
                       'lzma': True,
                       'iconv': True,
                       'freetype': True,
                       'openjpeg': True,
                       'openh264': True,
                       'opus': True,
                       'vorbis': True,
                       'zmq': False,
                       'sdl2': False,
                       'x264': True,
                       'x265': True,
                       'vpx': True,
                       'mp3lame': True,
                       'fdk_aac': True,
                       'webp': True,
                       'openssl': True,
                       'alsa': True,
                       'pulse': True,
                       'vaapi': True,
                       'vdpau': True,
                       'xcb': True,
                       'appkit': True,
                       'avfoundation': True,
                       'coreimage': True,
                       'audiotoolbox': True,
                       'videotoolbox': True,
                       'securetransport': False,  # conflicts with OpenSSL
                       'qsv': True}
    generators = "pkg_config"
    _source_subfolder = "source_subfolder"
    
    @property
    def _use_mingw(self):
        return self.settings.os == "Windows" and self.settings.compiler == "gcc"

    @property
    def _use_winbash(self):
        return tools.os_info.is_windows and (self.settings.compiler == 'gcc' or tools.cross_building(self.settings))

    @property
    def _is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url,
                  sha256="306bde5f411e9ee04352d1d3de41bd3de986e42e2af2a4c44052dce1ada26fb8")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.settings.os != "Linux":
            self.options.remove("vaapi")
            self.options.remove("vdpau")
            self.options.remove("xcb")
            self.options.remove("alsa")
            self.options.remove("pulse")
        if self.settings.os != "Macos":
            self.options.remove("appkit")
            self.options.remove("avfoundation")
            self.options.remove("coreimage")
            self.options.remove("audiotoolbox")
            self.options.remove("videotoolbox")
            self.options.remove("securetransport")
        if self.settings.os != "Windows":
            self.options.remove("qsv")

    def build_requirements(self):
        self.build_requires("yasm_installer/1.3.0@bincrafters/stable")
        if tools.os_info.is_windows:
            if "CONAN_BASH_PATH" not in os.environ:
                self.build_requires("msys2_installer/latest@bincrafters/stable")
            if tools.run_in_windows_bash(self, "which pkg-config") != 0:
                self.build_requires("pkg-config_installer/0.29.2@bincrafters/stable")
        if (self.settings.os == "Android" and tools.cross_building(self.settings)
            and not "android_ndk_installer" in self.deps_cpp_info.deps
            and not "NDK_ROOT" in os.environ):
            self.build_requires("android_ndk_installer/r20@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/1.0.8@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/5.2.4@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/2.10.0@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/2.3.1@bincrafters/stable")
        if self.options.openh264:
            self.requires.add("openh264/1.7.0@bincrafters/stable")
        if self.options.vorbis:
            self.requires.add("vorbis/1.3.6@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/1.3.1@bincrafters/stable")
        if self.options.zmq:
            self.requires.add("zmq/4.3.1@bincrafters/stable")
        if self.options.sdl2:
            self.requires.add("sdl2/2.0.9@bincrafters/stable")
        if self.options.x264:
            self.requires.add("libx264/20190605@bincrafters/stable")
        if self.options.x265:
            self.requires.add("libx265/3.0@bincrafters/stable")
        if self.options.vpx:
            self.requires.add("libvpx/1.8.0@bincrafters/stable")
        if self.options.mp3lame:
            self.requires.add("libmp3lame/3.100@bincrafters/stable")
        if self.options.fdk_aac:
            self.requires.add("libfdk_aac/2.0.0@bincrafters/stable")
        if self.options.webp:
            self.requires.add("libwebp/1.0.3@bincrafters/stable")
        if self.options.openssl:
            self.requires.add("OpenSSL/1.1.1c@conan/stable")
        if self.settings.os == "Windows":
            if self.options.qsv:
                self.requires.add("intel_media_sdk/2018R2_1@bincrafters/stable")

    def system_requirements(self):
        if not tools.cross_building(self.settings) and self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                arch_suffix = ''
                if self.settings.arch == "x86":
                    arch_suffix = ':i386'
                elif self.settings.arch == "x86_64":
                    arch_suffix = ':amd64'

                packages = ['pkg-config']
                if self.options.alsa:
                    packages.append('libasound2-dev%s' % arch_suffix)
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

    def _copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        for pc_name in pc_files:
            new_pc = os.path.basename(pc_name)
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            prefix = tools.unix_path(root) if self.settings.os == 'Windows' else root
            tools.replace_prefix_in_pc_file(new_pc, prefix)

    def _patch_sources(self):
        if self._is_msvc and self.options.x264 and not self.options['x264'].shared:
            # suppress MSVC linker warnings: https://trac.ffmpeg.org/ticket/7396
            # warning LNK4049: locally defined symbol x264_levels imported
            # warning LNK4049: locally defined symbol x264_bit_depth imported
            tools.replace_in_file(os.path.join(self._source_subfolder, 'libavcodec', 'libx264.c'),
                                  '#define X264_API_IMPORTS 1', '')
        if self.options.openssl:
            # https://trac.ffmpeg.org/ticket/5675
            openssl_libraries = ' '.join(['-l%s' % lib for lib in self.deps_cpp_info["OpenSSL"].libs])
            tools.replace_in_file(os.path.join(self._source_subfolder, 'configure'),
                                  'check_lib openssl openssl/ssl.h SSL_library_init -lssl -lcrypto -lws2_32 -lgdi32 ||',
                                  'check_lib openssl openssl/ssl.h OPENSSL_init_ssl %s || ' % openssl_libraries)

    def build(self):
        self._patch_sources()
        with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
            self.build_configure()

    def _format_path(self, path):
        return tools.unix_path(path) if self._use_winbash else path

    @property
    def _target_os(self):
        os = str(self.settings.os)
        if os == "Windows":
            return "mingw32" if self._use_mingw else "win32"
        elif os in ["Macos", "iOS", "watchOS", "tvOS"]:
            return "darwin"
        elif os in ["Linux", "Android", "FreeBSD", "SunOS", "AIX"]:
            return os.lower()
        else:
            raise ConanInvalidConfiguration("Unsupported os '{}'".format(os))

    def build_configure(self):
        # FIXME : once component feature is out, should be unnecessary
        if self.options.freetype:
            shutil.move("freetype.pc", "freetype2.pc")
        if self.options.openjpeg:
            shutil.move("openjpeg.pc", "libopenjp2.pc")
        if self.options.x264:
            shutil.move("libx264.pc", "x264.pc")
        if self.options.x265:
            shutil.move("libx265.pc", "x265.pc")
        if self.options.fdk_aac:
            shutil.move("libfdk_aac.pc", "fdk-aac.pc")
        if self.options.webp:
            shutil.move("libwebp.pc", "webp.pc")  # components: libwebpmux
        if self.options.vorbis:
            self._copy_pkg_config('vorbis')  # components: vorbisenc, vorbisfile
        with tools.chdir(self._source_subfolder):
            prefix = self._format_path(self.package_folder)
            args = ['--prefix=%s' % prefix,
                    '--disable-doc',
                    '--disable-programs']
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static'])
            args.append('--pkg-config-flags=--static')
            if self.settings.build_type == 'Debug':
                args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug'])
            if self._is_msvc:
                args.append('--toolchain=msvc')
                args.append('--extra-cflags=-%s' % self.settings.compiler.runtime)
                if int(str(self.settings.compiler.version)) <= 12:
                    # Visual Studio 2013 (and earlier) doesn't support "inline" keyword for C (only for C++)
                    args.append('--extra-cflags=-Dinline=__inline' % self.settings.compiler.runtime)

            if self.settings.arch == 'x86':
                args.append('--arch=x86')

            if self.settings.os != "Windows":
                args.append('--enable-pic' if self.options.fPIC else '--disable-pic')

            args.append('--enable-postproc' if self.options.postproc else '--disable-postproc')
            args.append('--enable-zlib' if self.options.zlib else '--disable-zlib')
            args.append('--enable-bzlib' if self.options.bzlib else '--disable-bzlib')
            args.append('--enable-lzma' if self.options.lzma else '--disable-lzma')
            args.append('--enable-iconv' if self.options.iconv else '--disable-iconv')
            args.append('--enable-libfreetype' if self.options.freetype else '--disable-libfreetype')
            args.append('--enable-libopenjpeg' if self.options.openjpeg else '--disable-libopenjpeg')
            args.append('--enable-libopenh264' if self.options.openh264 else '--disable-libopenh264')
            args.append('--enable-libvorbis' if self.options.vorbis else '--disable-libvorbis')
            args.append('--enable-libopus' if self.options.opus else '--disable-libopus')
            args.append('--enable-libzmq' if self.options.zmq else '--disable-libzmq')
            args.append('--enable-sdl2' if self.options.sdl2 else '--disable-sdl2')
            args.append('--enable-libx264' if self.options.x264 else '--disable-libx264')
            args.append('--enable-libx265' if self.options.x265 else '--disable-libx265')
            args.append('--enable-libvpx' if self.options.vpx else '--disable-libvpx')
            args.append('--enable-libmp3lame' if self.options.mp3lame else '--disable-libmp3lame')
            args.append('--enable-libfdk-aac' if self.options.fdk_aac else '--disable-libfdk-aac')
            args.append('--enable-libwebp' if self.options.webp else '--disable-libwebp')
            args.append('--enable-openssl' if self.options.openssl else '--disable-openssl')

            if self.options.x264 or self.options.x265 or self.options.postproc:
                args.append('--enable-gpl')

            if self.options.fdk_aac:
                args.append('--enable-nonfree')

            if self.settings.os == "Linux":
                args.append('--enable-alsa' if self.options.alsa else '--disable-alsa')
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
                args.append('--enable-securetransport' if self.options.securetransport else '--disable-securetransport')

            if self.settings.os == "Windows":
                args.append('--enable-libmfx' if self.options.qsv else '--disable-libmfx')

            if tools.cross_building(self.settings):
                args.append('--enable-cross-compile')
                args.append('--target-os=%s' % self._target_os)
                cc = os.environ["CC"]
                cxx = os.environ["CXX"]
                args.append('--cc=%s' % cc)
                args.append('--cxx=%s' % cxx)
                arch = {'armv7': 'arm',
                        'armv8': 'aarch64',
                        'x86': 'i686',
                        'x86_64': 'x86_64'}.get(str(self.settings.arch))
                args.append('--arch=%s' % arch)

                if self.settings.os == "Android":
                    ndk_root = self._format_path(os.environ["NDK_ROOT"])
                    abi = 'androideabi' if self.settings.arch == 'armv7' else 'android'
                    cross_prefix = "%s/bin/%s-linux-%s-" % (ndk_root, arch, abi)
                    args.append('--cross-prefix=%s' % cross_prefix)
                    # if not specified, it will be set to cross_prefix-pkg-config by default
                    # which does not exist in ndk
                    args.append('--pkg-config=pkg-config')

            # FIXME disable CUDA and CUVID by default, revisit later
            args.extend(['--disable-cuda', '--disable-cuvid'])

            env_build = AutoToolsBuildEnvironment(self, win_bash=self._use_winbash or self._is_msvc)
            # ffmpeg's configure is not actually from autotools, so it doesn't understand standard options like
            # --host, --build, --target
            env_build.configure(args=args, build=False, host=False, target=False)
            env_build.make()
            env_build.make(args=['install'])

    def package(self):
        with tools.chdir(self._source_subfolder):
            self.copy(pattern="LICENSE")
        if self._is_msvc and not self.options.shared:
            # ffmpeg produces .a files which are actually .lib files
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                libs = glob.glob('*.a')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.lib')

    def run(self, *args, **kwargs):
        # ensure PKG_CONFIG_PATH is inherited by MSYS bash
        kwargs["with_login"] = False
        super(FFMpegConan, self).run(*args, **kwargs)

    def package_info(self):
        libs = ['avdevice', 'avfilter', 'avformat', 'avcodec', 'swresample', 'swscale', 'avutil']
        if self.options.postproc:
            libs.append('postproc')
        if self._is_msvc:
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
            if self.options.securetransport:
                frameworks.append('Security')
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
            if self.options.alsa:
                self.cpp_info.libs.append('asound')
            if self.options.pulse:
                self.cpp_info.libs.append('pulse')
            if self.options.vaapi:
                self.cpp_info.libs.extend(['va', 'va-drm', 'va-x11'])
            if self.options.vdpau:
                self.cpp_info.libs.extend(['vdpau', 'X11'])
            if self.options.xcb:
                self.cpp_info.libs.extend(['xcb', 'xcb-shm', 'xcb-shape', 'xcb-xfixes'])
            if self.settings.os != "Windows" and self.options.fPIC:
                # https://trac.ffmpeg.org/ticket/1713
                # https://ffmpeg.org/platform.html#Advanced-linking-configuration
                # https://ffmpeg.org/pipermail/libav-user/2014-December/007719.html
                self.cpp_info.sharedlinkflags.append("-Wl,-Bsymbolic")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32', 'bcrypt'])
