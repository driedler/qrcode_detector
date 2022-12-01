


add_executable(${PROJECT_NAME}_example)
target_sources(${PROJECT_NAME}_example
PRIVATE 
    main.cpp
)

target_link_libraries(${PROJECT_NAME}_example
PRIVATE 
  OpenCV_GUI
  qrcode_detector
)