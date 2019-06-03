cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../server ${CMAKE_CURRENT_BINARY_DIR}/server)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../client ${CMAKE_CURRENT_BINARY_DIR}/client)
include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/../server
	${CMAKE_CURRENT_SOURCE_DIR}/../client
)
add_executable(main ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)
set_property(TARGET main PROPERTY CXX_STANDARD 11)
target_link_libraries(main server client)
