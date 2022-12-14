

add_subdirectory(pybind11)


# This is the name of the generated DLL/shared library
set(MODULE_NAME _qrcode_detector)
add_custom_target(${PROJECT_NAME}_wrapper
  DEPENDS ${MODULE_NAME}
)

# Define the pybind11 wrapper target
pybind11_add_module(${MODULE_NAME} SHARED
  qrcode_detector_pybind11.cc
)


# Set additional build properties
set_target_properties(${MODULE_NAME} PROPERTIES
  OPT_SIZE ON
  INTERPROCEDURAL_OPTIMIZATION ON
  CXX_VISIBILITY_PRESET hidden
  VISIBLITY_INLINES_HIDDEN ON
)

target_link_libraries(${MODULE_NAME} 
PUBLIC 
  qrcode_detector
)

target_include_directories(${MODULE_NAME} 
PUBLIC 
  ${CMAKE_CURRENT_LIST_DIR}/cpp
)

target_compile_features(${MODULE_NAME}  
PUBLIC 
  cxx_std_17
)

if(NOT MSVC)
  target_link_options(${MODULE_NAME}
  PUBLIC
    -Wl,-Map,${CMAKE_CURRENT_BINARY_DIR}/output.map
  )
endif()

target_compile_definitions(${MODULE_NAME}
PRIVATE
    MODULE_NAME=${MODULE_NAME}
)

# Copy the built .pyd/.so to the directory:
# <mltk root>/mltk/core/preprocess/audio/audio_feature_generator
get_filename_component(qrcode_detector_python_dir "${CMAKE_CURRENT_LIST_DIR}/../../qrcode_detector" ABSOLUTE)
add_custom_command(
  TARGET ${MODULE_NAME} 
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${MODULE_NAME}> ${qrcode_detector_python_dir}
  COMMAND ${CMAKE_COMMAND} -E echo "Copying built wrapper to ${qrcode_detector_python_dir}/$<TARGET_FILE_NAME:${MODULE_NAME}>"
)

