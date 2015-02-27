cmake_minimum_required(VERSION 2.8.12.2 FATAL_ERROR)

file(GLOB src "hello.c")

add_library(Hello ${src})
