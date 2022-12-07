#include <string>
#include <opencv2/core/core.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>


#include "CodeFinder.hpp"

namespace py = pybind11;

// This works around link error on ARM
uintptr_t __pointer_chk_guard_local;


PYBIND11_MODULE(MODULE_NAME, m) 
{
    m.def("find_and_decode", [](const py::array& image) -> std::string
    {
        auto shape = image.shape();

        if (!image.dtype().is(py::dtype::of<uchar>()) || image.ndim() != 3) {
            throw py::value_error("Input image must be 3D uint8");
        }

        int rows = shape[0];
        int cols = shape[1];
        int channels = shape[2];

        int type = CV_MAKETYPE(CV_8U, channels); // CV_8UC3
        cv::Mat mat = cv::Mat(rows, cols, type);
        memcpy(mat.data, image.data(), sizeof(uchar) * rows * cols * channels);

        CodeFinder finder(mat);
        return finder.findAndDecode();
    })

    ;
}