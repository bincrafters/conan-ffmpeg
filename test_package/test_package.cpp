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

static void check_decoder(const char * name)
{
    if (!avcodec_find_decoder_by_name(name)) {
        std::stringstream s;
        s << "encoder wasn't found - " << name;
        throw std::runtime_error(s.str().c_str());
    }
}

static void check_encoder(const char * name)
{
    if (!avcodec_find_encoder_by_name(name)) {
        std::stringstream s;
        s << "encoder wasn't found - " << name;
        throw std::runtime_error(s.str().c_str());
    }
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
}
