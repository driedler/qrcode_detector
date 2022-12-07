
set(BUILD_LIST "core,imgproc,objdetect" CACHE INTERNAL "")
CPMAddPackage(
    NAME OpenCV
    GITHUB_REPOSITORY opencv/opencv
    GIT_TAG 4.6.0
    CACHE_VERSION 4.6.0
    DOWNLOAD_ONLY
    OPTIONS 
         "BUILD_PACKAGE OFF"
         "BUILD_SHARED_LIBS OFF"
         "ENABLE_PIC  ON"
         "BUILD_ZLIB ON"
         "WITH_OPENCL OFF"
         "WITH_WEBP OFF"
         "WITH_JPEG OFF"
         "WITH_TIFF OFF"
         "WITH_PROTOBUF OFF"
         "WITH_IMGCODEC_HDR OFF"
         "WITH_IMGCODEC_SUNRASTER OFF",
         "WITH_IMGCODEC_PXM OFF",
         "WITH_IMGCODEC_PFM OFF",
         "WITH_PNG OFF"
         "WITH_PTHREADS_PF OFF",
         "OPENCV_FORCE_3RDPARTY_BUILD ON"
         "OPENCV_DISABLE_FILESYSTEM_SUPPORT ON"
         "WITH_ITT OFF"
)

add_library(OpenCV_Basic INTERFACE)
target_include_directories(OpenCV_Basic
INTERFACE
"${OpenCV_SOURCE_DIR}/include" 
"${OpenCV_SOURCE_DIR}/modules/core/include" 
"${OpenCV_SOURCE_DIR}/modules/imgproc/include" 
"${OpenCV_SOURCE_DIR}/modules/objdetect/include" 
"${OpenCV_SOURCE_DIR}/modules/highgui/include" 
"${OpenCV_SOURCE_DIR}/modules/imgcodecs/include" 
"${OpenCV_SOURCE_DIR}/modules/video/include" 
"${OpenCV_SOURCE_DIR}/modules/videoio/include" 
"${CMAKE_CURRENT_LIST_DIR}"
)
target_link_libraries(OpenCV_Basic
INTERFACE
    opencv_core 
    opencv_imgproc  
    opencv_objdetect
)

add_library(OpenCV_GUI INTERFACE)
target_link_libraries(OpenCV_GUI
INTERFACE
    OpenCV_Basic
    opencv_highgui 
    opencv_video 
    opencv_gapi
    opencv_imgcodecs
)
