cmake_minimum_required(VERSION 3.15.1)
project(QRCodeDetector
  VERSION 1.0.0
  DESCRIPTION "Robust implementation for detecting QR codes using OpenCV"
)

# cmake_policy(SET CMP0091 NEW)
# set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>" CACHE INTERNAL "")

if(NOT MSVC)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fvisibility=hidden -fPIC" CACHE INTERNAL "")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fvisibility=hidden -fPIC" CACHE INTERNAL "")
endif()



###################################################################################################
# Add the build dependencies
set(CPM_SOURCE_CACHE "${CMAKE_CURRENT_LIST_DIR}" CACHE INTERNAL "CPM cache directory")
include(${CMAKE_CURRENT_LIST_DIR}/CPM.cmake)
add_subdirectory(opencv)
add_subdirectory(qrcode_detector)
add_subdirectory(wrapper)

