cmake_minimum_required(VERSION 2.8.12.2 FATAL_ERROR)

file(GLOB src "class.cpp")

add_library(Class ${src})
