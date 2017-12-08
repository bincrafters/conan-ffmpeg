#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)

        cmake.definitions['WITH_OPENJPEG'] = self.options['ffmpeg'].openjpeg
        cmake.definitions['WITH_FREETYPE'] = self.options['ffmpeg'].freetype
        cmake.definitions['WITH_VORBIS'] = self.options['ffmpeg'].vorbis

        if self.settings.os == "Linux":
            cmake.definitions['WITH_VAAPI'] = self.options['ffmpeg'].vaapi
            cmake.definitions['WITH_VDPAU'] = self.options['ffmpeg'].vdpau
            cmake.definitions['WITH_XCB'] = self.options['ffmpeg'].xcb

        if self.settings.os == "Macos":
            cmake.definitions['WITH_APPKIT'] = self.options['ffmpeg'].appkit
            cmake.definitions['WITH_AVFOUNDATION'] = self.options['ffmpeg'].avfoundation
            cmake.definitions['WITH_COREIMAGE'] = self.options['ffmpeg'].coreimage
            cmake.definitions['WITH_AUDIOTOOLBOX'] = self.options['ffmpeg'].audiotoolbox
            cmake.definitions['WITH_VIDEOTOOLBOX'] = self.options['ffmpeg'].videotoolbox
            cmake.definitions['WITH_VDA'] = self.options['ffmpeg'].vda
            cmake.definitions['WITH_SECURETRANSPORT'] = self.options['ffmpeg'].securetransport

        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
