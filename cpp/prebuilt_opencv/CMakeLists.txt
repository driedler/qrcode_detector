

if(WIN32)
    set(OPENCV_DOWNLOAD_URL "https://github.com/opencv/opencv/releases/download/4.6.0/opencv-4.6.0-vc14_vc15.exe")
    set(OPENCV_DOWNLOAD_HASH "3fb046e14dc5b50719a86ea0395b5b1e3299e2343111ebd2e31828aa31d6d477")
elseif(ANDROID)
    set(OPENCV_DOWNLOAD_URL "https://github.com/opencv/opencv/releases/download/4.6.0/opencv-4.6.0-android-sdk.zip")
    set(OPENCV_DOWNLOAD_HASH "b1f0002af4792866edbfde6a85346deb78a79c68b019f2d6f13cee7e08cef0aa")
else()
    message(FATAL "OS not supported")
endif()


CPMAddPackage(
    NAME prebuilt_opencv
    URL  ${OPENCV_DOWNLOAD_URL}
    URL_HASH SHA256=${OPENCV_DOWNLOAD_HASH}
    CACHE_VERSION 4.6.0
    DOWNLOAD_ONLY
)
set(OpenCV_DIR "${CMAKE_CURRENT_LIST_DIR}/4.6.0/build")

find_package(OpenCV REQUIRED)
message(STATUS "OpenCV_LIBS=${OpenCV_LIBS}")
message(STATUS "OpenCV_INCLUDE_DIRS=${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV_LIB_PATH=${OpenCV_LIB_PATH}")

add_library(prebuilt_opencv INTERFACE)

target_include_directories(prebuilt_opencv INTERFACE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(prebuilt_opencv INTERFACE ${OpenCV_LIBS})

if(CMAKE_BUILD_TYPE MATCHES DEBUG)
    set(_opencv_lib_ext d)
endif()
if(WIN32)
    set(_opencv_lib_ext "${_opencv_lib_ext}.dll")
endif()

get_filename_component(_opencv_shared_lib_path "${OpenCV_LIB_PATH}/../bin/opencv_world460${_opencv_lib_ext}" ABSOLUTE CACHE)

function(copy_prebuilt_opencv_libs target)
    add_custom_command(
    TARGET ${target} 
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy "${_opencv_shared_lib_path}" $<TARGET_FILE_DIR:${target}>
    )
endfunction()