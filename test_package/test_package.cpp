extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavfilter/avfilter.h>
#include <libavdevice/avdevice.h>
#include <libswresample/swresample.h>
#include <libswscale/swscale.h>
#include <libavutil/hwcontext.h>
}

#include <stdexcept>
#include <string>
#include <sstream>
#include <iostream>

static void throw_exception(const char * message, const char * name)
{
    std::stringstream s;
    s << message << " - " << name;
    throw std::runtime_error(s.str().c_str());
}

static void check_decoder(const char * name)
{
    std::cout << "checking for decoder " << name << " ..." << std::endl;
    if (!avcodec_find_decoder_by_name(name))
        throw_exception("decoder wasn't found", name);
}

static void check_encoder(const char * name)
{
    std::cout << "checking for encoder " << name << " ..." << std::endl;
    if (!avcodec_find_encoder_by_name(name))
        throw_exception("encoder wasn't found", name);
}

static void check_filter(const char * name)
{
    std::cout << "checking for filter " << name << " ..." << std::endl;
    if (!avfilter_get_by_name(name))
        throw_exception("filter wasn't found", name);
}

static void check_hwaccel(const char * name)
{
    std::cout << "checking for hwaccel " << name << " ..." << std::endl;
    AVHWDeviceType type = av_hwdevice_find_type_by_name(name);
    if (type == AV_HWDEVICE_TYPE_NONE)
        throw_exception("hwaccel wasn't found", name);
    if (!av_hwdevice_ctx_alloc(type))
        throw_exception("hwaccel wasn't found", name);
}

int main()
{
    avcodec_register_all();
    av_register_all();
    avfilter_register_all();
    avdevice_register_all();
    swresample_version();
    swscale_version();

#ifdef WITH_OPENJPEG
    check_decoder("libopenjpeg");
    check_encoder("libopenjpeg");
#endif
#ifdef WITH_FREETYPE
    check_filter("drawtext");
#endif
#ifdef WITH_VAAPI
    check_hwaccel("vaapi");
#endif
#ifdef WITH_VDPAU
    check_hwaccel("vdpau");
#endif
#ifdef WITH_VORBIS
    check_decoder("libvorbis");
    check_encoder("libvorbis");
#endif
}
