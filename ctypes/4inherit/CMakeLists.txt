cmake_minimum_required(VERSION 2.8.12.2 FATAL_ERROR)

file(GLOB derived_src "derived.cpp")
file(GLOB polymorph_src "polymorph.cpp")

add_library(Derived ${derived_src})
add_library(Polymorph ${polymorph_src})
