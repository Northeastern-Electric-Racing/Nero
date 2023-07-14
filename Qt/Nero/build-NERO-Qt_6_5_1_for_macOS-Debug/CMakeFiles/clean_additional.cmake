# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles/NERO_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/NERO_autogen.dir/ParseCache.txt"
  "NERO_autogen"
  )
endif()
