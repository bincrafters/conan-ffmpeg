[![Download](https://api.bintray.com/packages/bincrafters/public-conan/ffmpeg%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/ffmpeg%3Abincrafters/_latestVersion)
[![Build Status](https://travis-ci.org/bincrafters/conan-ffmpeg.svg?branch=stable%2F3.4)](https://travis-ci.org/bincrafters/conan-ffmpeg)
[![Build status](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-ffmpeg?branch=stable%2F3.4&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-ffmpeg)

[Conan.io](https://conan.io) package recipe for *ffmpeg*.

A complete, cross-platform solution to record, convert and stream audio and video

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/ffmpeg%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install ffmpeg/3.4@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ffmpeg/3.4@bincrafters/stable


Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bincrafters/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| xcb      | True |  [True, False] |
| pulse      | True |  [True, False] |
| vorbis      | True |  [True, False] |
| lzma      | True |  [True, False] |
| iconv      | True |  [True, False] |
| bzlib      | True |  [True, False] |
| opus      | True |  [True, False] |
| avfoundation      | True |  [True, False] |
| shared      | False |  [True, False] |
| zmq      | True |  [True, False] |
| alsa      | True |  [True, False] |
| freetype      | False |  [True, False] |
| audiotoolbox      | True |  [True, False] |
| fPIC      | True |  [True, False] |
| videotoolbox      | True |  [True, False] |
| coreimage      | True |  [True, False] |
| appkit      | True |  [True, False] |
| openjpeg      | True |  [True, False] |
| securetransport      | True |  [True, False] |
| vdpau      | True |  [True, False] |
| zlib      | True |  [True, False] |
| vda      | False |  [True, False] |
| vaapi      | True |  [True, False] |
| jack      | True |  [True, False] |

## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload ffmpeg/3.4@bincrafters/stable --all -r bincrafters


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package ffmpeg.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-ffmpeg.git/blob/testing/3.4/LICENSE.md)
