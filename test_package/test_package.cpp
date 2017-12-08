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
#include <cstdlib>

static void throw_exception(const char * message, const char * name)
{
    std::stringstream s;
    s << message << " - " << name;
    throw std::runtime_error(s.str().c_str());
}

static void check_decoder(const char * name)
{
    std::cout << "checking for decoder " << name << " ... ";
    if (!avcodec_find_decoder_by_name(name))
        throw_exception("decoder wasn't found", name);
    std::cout << "OK!" << std::endl;
}

static void check_encoder(const char * name)
{
    std::cout << "checking for encoder " << name << " ... ";
    if (!avcodec_find_encoder_by_name(name))
        throw_exception("encoder wasn't found", name);
    std::cout << "OK!" << std::endl;
}

static void check_filter(const char * name)
{
    std::cout << "checking for filter " << name << " ... ";
    if (!avfilter_get_by_name(name))
        throw_exception("filter wasn't found", name);
    std::cout << "OK!" << std::endl;
}

static void check_hwaccel(const char * name)
{
    std::cout << "checking for hwaccel " << name << " ... ";
    AVHWDeviceType type = av_hwdevice_find_type_by_name(name);
    if (type == AV_HWDEVICE_TYPE_NONE)
        throw_exception("hwaccel wasn't found", name);
    if (!av_hwdevice_ctx_alloc(type))
        throw_exception("hwaccel wasn't found", name);
    std::cout << "OK!" << std::endl;
}

static void check_input_device(const char * name)
{
    std::cout << "checking for device " << name << " ... ";

    if (!av_find_input_format(name))
        throw_exception("device wasn't found", name);
    std::cout << "OK!" << std::endl;
}

static void check_protocol(const char * name)
{
    std::cout << "checking for protocol " << name << " ... ";

    bool found = false;

    const char * protocol = NULL;
    void* dontcare = NULL;

    while ((protocol = avio_enum_protocols(&dontcare, 0))) {
        if (0 == strcmp(name, protocol)) {
            found = true;
            break;
        }
    }

    if (found) {
        std::cout << "OK!" << std::endl;
        return;
    }

    while ((protocol = avio_enum_protocols(&dontcare, 1))) {
        if (0 == strcmp(name, protocol)) {
            found = true;
            break;
        }
    }

    if (!found)
        throw_exception("protocol wasn't found", name);
    std::cout << "OK!" << std::endl;
}

int main() try
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
#ifdef WITH_XCB
    check_input_device("x11grab");
#endif
#if defined(WITH_APPKIT) && defined(WITH_COREIMAGE)
    check_filter("coreimage");
#endif
#ifdef WITH_AVFOUNDATION
    check_input_device("avfoundation");
#endif
#ifdef WITH_AUDIOTOOLBOX
    check_decoder("aac_at");
#endif
#ifdef WITH_VIDEOTOOLBOX
    check_hwaccel("videotoolbox");
#endif
#ifdef WITH_VDA
    check_hwaccel("h264_vda");
#endif
#ifdef WITH_SECURETRANSPORT
    check_protocol("tls");
#endif
    return EXIT_SUCCESS;
} catch (std::runtime_error & e)
{
    std::cout << "FAIL!" << std::endl;
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
