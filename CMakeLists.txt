# CSRHOS - Chinese Solar Radio HelioGraph Operation System
# MUSEROS - Mingantu Ultrawide Spectral Radio Heliograph
#
# Author: CNLABers
# Created: Since 2013-1-1
#
# This file is part of CSRH/MUSER project
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Version required >= 2.6
cmake_minimum_required( VERSION 2.6 )


set( MUSER_MAJOR_VERSION 1 )
set( MUSER_MINOR_VERSION 0 )
set( MUSER_PATCH_VERSION 0 )
set( MUSER_API_VERSION "${MUSER_MAJOR_VERSION}.${MUSER_MINOR_VERSION}.${MUSER_PATCH_VERSION}" )


#enable_language (Fortran)

PROJECT (MUSEROS C CXX)

#Search Python Interpretor
# C/C++ and Fortran Compiler

if("${CMAKE_SYSTEM}" MATCHES "Darwin")
#AND
#   CMAKE_SYSTEM_PROCESSOR STREQUAL x86_64 )
    set( SO so)
    if( EXISTS ${CMAKE_Fortran_COMPILER})
        message(STATUS "Use " ${CMAKE_Fortran_COMPILER})
    endif()
    if( EXISTS /usr/local/bin/gfortran )
        set( CMAKE_Fortran_COMPILER /usr/local/bin/gfortran )
    elseif( EXISTS /usr/bin/gfortran )
        set( CMAKE_Fortran_COMPILER /usr/bin/gfortran )
    endif()
    if( EXISTS /usr/local/bin/g++)
      	set( CMAKE_CXX_COMPILER     /usr/local/bin/g++ )
    elseif( EXISTS /usr/bin/g++ )
      	set( CMAKE_CXX_COMPILER     /usr/bin/g++ )
    endif()
    if( EXISTS /usr/local/bin/gcc)
      	set( CMAKE_C_COMPILER     /usr/local/bin/gcc )
    elseif( EXISTS /usr/bin/gcc )
      	set( CMAKE_C_COMPILER     /usr/bin/gcc )
    endif()
else()
    set( SO so )
endif()

if("${CMAKE_SYSTEM}" MATCHES "Darwin")
  foreach( _c CXX C FORTRAN )
    set( CMAKE_${_c}_FLAGS " -O2 -fPIC -flat_namespace")
  endforeach()
endif()

if("${CMAKE_SYSTEM}" MATCHES "Linux")
  foreach( _c CXX C FORTRAN )
    set( CMAKE_${_c}_FLAGS " -O2 -fPIC")
  endforeach()
  #set( PYTHON_INCLUDE_PATH /usr/local/include/python2.7)
  #set( PYTHON_LIBRARIES /usr/local/lib/python2.7)
endif()


# On Linux x86_64 add the (gcc specific) -fno-omit-frame-pointer
# flag to debug builds
# If possible, x86_64 and 64bits libraries are used.


# Search all packages needed
#
# CFITSIO and other packages are needed.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")
set_property(GLOBAL PROPERTY FIND_LIBRARY_USE_LIB64_PATHS ON)

FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs)
SET(CMAKE_SWIG_FLAGS "")

FIND_PACKAGE(CFITSIO REQUIRED)
#INCLUDE(${CFITSIO_INCLUDE_DIR})
include_directories(${CFITSIO_INCLUDE_DIRS})
#FIND_PACKAGE(ZMQ REQUIRED)
#FIND_PACKAGE(MYSQL REQUIRED)
#INCLUDE(${MYSQL_INCLUDE_DIR})
#include_directories(${MYSQL_INCLUDE_DIRS})


INCLUDE_DIRECTORIES(
${CMAKE_SOURCE_DIR}/src/ephem
${CMAKE_SOURCE_DIR}/include
${PYTHON_INCLUDE_PATH}
${CMAKE_CURRENT_SOURCE_DIR}
${CFITSIO_INCLUDE_DIR}
)

LINK_DIRECTORIES(
/usr/local/lib
/usr/lib
)

# Project information - MUSEROS

ADD_SUBDIRECTORY(src)

IF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  SET(CMAKE_INSTALL_PREFIX
    $ENV{HOME}/museros CACHE PATH "MUSEROS install prefix" FORCE
    )
ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)

SET(CMAKE_INSTALL_PREFIX $ENV{HOME}/museros)

#SET(CMAKE_INSTALL_PREFIX  "~/museros" )

#INSTALL(FILES COPYRIGHT README DESTINATION doc)
#INSTALL(DIRECTORY src/scripts/ DESTINATION scripts)

#INSTALL(DIRECTORY test/ DESTINATION test
#     PATTERN "*"
#     PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ)

INSTALL(DIRECTORY data/ DESTINATION data
     PATTERN "*"
     PERMISSIONS
     OWNER_WRITE OWNER_READ OWNER_EXECUTE
     GROUP_WRITE GROUP_READ GROUP_EXECUTE
     WORLD_WRITE WORLD_READ WORLD_EXECUTE)

INSTALL(DIRECTORY shell/ DESTINATION bin
     PATTERN "*"
     PERMISSIONS
     OWNER_WRITE OWNER_READ OWNER_EXECUTE
     GROUP_WRITE GROUP_READ GROUP_EXECUTE
     WORLD_WRITE WORLD_READ WORLD_EXECUTE)

INSTALL(DIRECTORY db/ DESTINATION db
     PATTERN "*"
     PERMISSIONS
     OWNER_WRITE OWNER_READ OWNER_EXECUTE
     GROUP_WRITE GROUP_READ GROUP_EXECUTE
     WORLD_WRITE WORLD_READ WORLD_EXECUTE)
