cmake_minimum_required(VERSION 3.5.1)
project(QRCode
VERSION 1.0.0
DESCRIPTION "Robust implementation for detecting QR codes using OpenCV"
)


set(CPM_SOURCE_CACHE "${CMAKE_CURRENT_LIST_DIR}/cpp" CACHE INTERNAL "CPM cache directory")
include(${CMAKE_CURRENT_LIST_DIR}/cpp/CPM.cmake)


add_library(${PROJECT_NAME})

add_subdirectory(cpp/prebuilt_opencv)

target_compile_features(${PROJECT_NAME}
PUBLIC 
cxx_std_11
)

target_sources(${PROJECT_NAME}
PRIVATE
    cpp/CodeFinder.hpp
    cpp/CodeFinder.cpp 
    cpp/FinderPatternModel.hpp 
    cpp/ImageBinarization.cpp
    cpp/ImageBinarization.hpp 
)



target_link_libraries(${PROJECT_NAME} 
PUBLIC
    prebuilt_opencv
)

add_executable(${PROJECT_NAME}_example)
target_sources(${PROJECT_NAME}_example
PRIVATE 
    cpp/main.cpp
)
copy_prebuilt_opencv_libs(${PROJECT_NAME}_example)
target_link_libraries(${PROJECT_NAME}_example
PRIVATE 
    ${PROJECT_NAME}
)

target_compile_options(${PROJECT_NAME}  PUBLIC /wd4244)

