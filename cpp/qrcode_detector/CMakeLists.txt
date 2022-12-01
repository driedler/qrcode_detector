add_library(qrcode_detector)

target_compile_options(qrcode_detector  PUBLIC /wd4244)
target_compile_features(qrcode_detector
PUBLIC 
    cxx_std_11
)


target_include_directories(qrcode_detector
PUBLIC 
  ${CMAKE_CURRENT_LIST_DIR}
)

target_sources(qrcode_detector
PRIVATE
    CodeFinder.hpp
    CodeFinder.cpp 
    ImageBinarization.cpp
)

target_link_libraries(qrcode_detector
PUBLIC
  OpenCV_Basic
)
