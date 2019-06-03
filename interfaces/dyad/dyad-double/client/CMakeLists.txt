cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../dyad-dryad ${CMAKE_CURRENT_BINARY_DIR}/dryad)
add_library(client ${CMAKE_CURRENT_SOURCE_DIR}/client.cpp)
use_dryad(client)
