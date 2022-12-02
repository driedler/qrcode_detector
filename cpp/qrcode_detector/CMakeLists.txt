
macro(_define_library target)
  cmake_parse_arguments(_args "" "TYPE" "" ${ARGN})
  add_library(${target} ${_args_TYPE})
  target_compile_features(${target}
  PUBLIC 
      cxx_std_11
  )

  target_include_directories(${target}
  PUBLIC 
    ${CMAKE_CURRENT_LIST_DIR}
  )

  target_sources(${target}
  PRIVATE
      CodeFinder.hpp
      CodeFinder.cpp 
      ImageBinarization.cpp
  )

  target_link_libraries(${target}
  PUBLIC
    OpenCV_Basic
  )

  if(MSVC)
    target_compile_options(${target}  PUBLIC /wd4244)
  endif()
endmacro()


_define_library(qrcode_detector)
_define_library(qrcode_detector_shared TYPE SHARED)