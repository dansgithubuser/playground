cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)

set(dryad_include_directory ${CMAKE_CURRENT_SOURCE_DIR} PARENT_SCOPE)

if(NOT TARGET dryad)
	add_library(dryad
		${CMAKE_CURRENT_SOURCE_DIR}/dryad.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src/dyad.c
	)
	set_property(TARGET dryad PROPERTY CXX_STANDARD 11)
	include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src)
	target_include_directories(dryad PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src)
	target_link_libraries(dryad ws2_32)

	function(use_dryad target)
		target_include_directories(${target} PRIVATE ${dryad_include_directory})
		if(WIN32)
			target_link_libraries(${target} dryad)
		endif()
		set_property(TARGET ${target} PROPERTY CXX_STANDARD 11)
	endfunction()
endif()
