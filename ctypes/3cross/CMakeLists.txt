cmake_minimum_required(VERSION 2.8.12.2 FATAL_ERROR)

file(GLOB a_src "a.cpp")
file(GLOB b_src "b.cpp")

add_library(A ${a_src})
add_library(B ${b_src})
