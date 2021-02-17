#========================================================#
# Build the Boost dependencies for the project using a specific version of python #
#========================================================#

set(BoostVersion 1.75.0)
set(BoostMD5 ea217ed7c4414e93d44106c316966ae1)


string(REGEX REPLACE "beta\\.([0-9])$" "beta\\1" BoostFolderName ${BoostVersion})
string(REPLACE "." "_" BoostFolderName ${BoostFolderName})
set(BoostFolderName boost_${BoostFolderName})
message(STATUS "BoostFolderName= ${BoostFolderName}")
message(STATUS "Boost URL = http://sourceforge.net/projects/boost/files/boost/${BoostVersion}/${BoostFolderName}.tar.bz2/download")

ExternalProject_Add(Boost
    PREFIX Boost
    URL  http://sourceforge.net/projects/boost/files/boost/${BoostVersion}/${BoostFolderName}.tar.bz2/download
    URL_MD5 ${BoostMD5}
    CONFIGURE_COMMAND ./bootstrap.sh
                                                        --with-libraries=python
                                                        --with-python=${PYTHON_EXECUTABLE}
    BUILD_COMMAND           ./b2 install
                                                        variant=release
                                                        link=static
                                                        cxxflags='-fPIC'
                                                        --prefix=${CMAKE_BINARY_DIR}/extern
                                                        -d 0
                                                        -j8
    INSTALL_COMMAND ""
    BUILD_IN_SOURCE 1
    )

set(Boost_LIBRARY_DIR ${CMAKE_BINARY_DIR}/extern/lib/ )
set(Boost_INCLUDE_DIR ${CMAKE_BINARY_DIR}/extern/include/boost/ )

message(STATUS "PYTHON_VERSION_STRING = ${PYTHON_VERSION_STRING}")
string(REGEX REPLACE ".[0-9]$" "" PYTHON_VER ${PYTHON_VERSION_STRING})
string(REPLACE "." "" PYTHON_VER ${PYTHON_VER})
message(STATUS "PYTHON_VER = ${PYTHON_VER}")

if(${PYTHON_VERSION_STRING} GREATER 3.0)
  message(STATUS "Using Python${PYTHON_VER}")
  set(Boost_LIBRARIES -lboost_python${PYTHON_VER} -lboost_numpy${PYTHON_VER})
else()
  message(STATUS "Using Python2")
  set(Boost_LIBRARIES -lboost_python -lboost_numpy)
endif()
