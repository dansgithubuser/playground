cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src)

add_executable(
	chat
	${CMAKE_CURRENT_SOURCE_DIR}/chat.c
	${CMAKE_CURRENT_SOURCE_DIR}/../dyad/src/dyad.c
)

if(WIN32)
	target_link_libraries(chat ws2_32)
endif()
