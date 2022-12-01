
CPMAddPackage(
    NAME OpenCV
    GITHUB_REPOSITORY opencv/opencv
    GIT_TAG 4.6.0
    CACHE_VERSION 4.6.0
    DOWNLOAD_ONLY
    OPTIONS 
        "BUILD_PACKAGE OFF"
        "BUILD_SHARED_LIBS OFF"
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
