cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src)
message(STATUS "dryad_prefix is '${dryad_prefix}'")
add_definitions(-DDRYAD_PREFIX=\"${dryad_prefix}\")
add_library(${dryad_prefix}dryad OBJECT
	${CMAKE_CURRENT_SOURCE_DIR}/dryad.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src/dyad.c
)

set(dryad_include_directory ${CMAKE_CURRENT_SOURCE_DIR} PARENT_SCOPE)

function(use_dryad target)
	target_include_directories(${target} PRIVATE ${dryad_include_directory})
	if(WIN32)
		target_link_libraries(${target} ws2_32)
	endif()
endfunction()

function(add_dryad_library target source)
	add_library(${target} ${source} $<TARGET_OBJECTS:${dryad_prefix}dryad>)
	use_dryad(${target})
endfunction()
