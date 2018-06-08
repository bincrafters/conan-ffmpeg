#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


from bincrafters import build_template_default
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        modified_options = options.copy()
        if platform.system() == 'Linux':
            modified_options['ffmpeg:iconv'] = 'False'
            modified_options['ffmpeg:vdpau'] = 'False'
            modified_options['ffmpeg:vaapi'] = 'False'
            modified_options['ffmpeg:xcb'] = 'False'
        elif platform.system() == 'Windows':
            modified_options['ffmpeg:iconv'] = 'False'
            modified_options['ffmpeg:qsv'] = 'False'
        filtered_builds.append([settings, modified_options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
