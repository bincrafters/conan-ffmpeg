extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavfilter/avfilter.h>
#include <libavdevice/avdevice.h>
#include <libswresample/swresample.h>
#include <libswscale/swscale.h>
}

int main()
{
    avcodec_register_all();
    av_register_all();
    avfilter_register_all();
    avdevice_register_all();
    swresample_version();
    swscale_version();
}
