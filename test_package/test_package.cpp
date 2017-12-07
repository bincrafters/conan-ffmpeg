extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavfilter/avfilter.h>
#include <libavdevice/avdevice.h>
#include <libswresample/swresample.h>
#include <libswscale/swscale.h>
}

#include <stdexcept>
#include <string>
#include <sstream>

static void throw_exception(const char * message, const char * name)
{
    std::stringstream s;
    s << message << " - " << name;
    throw std::runtime_error(s.str().c_str());
}

static void check_decoder(const char * name)
{
    if (!avcodec_find_decoder_by_name(name))
        throw_exception("decoder wasn't found", name);
}

static void check_encoder(const char * name)
{
    if (!avcodec_find_encoder_by_name(name))
        throw_exception("encoder wasn't found", name);
}

static void check_filter(const char * name)
{
    if (!avfilter_get_by_name(name))
        throw_exception("filter wasn't found", name);
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
}
