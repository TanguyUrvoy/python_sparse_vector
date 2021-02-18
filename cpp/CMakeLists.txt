cmake_minimum_required(VERSION 2.8)
include(ExternalProject)

# Ajout d'un module cmake personnalisé pour générer boost
list(APPEND CMAKE_MODULE_PATH  "${CMAKE_SOURCE_DIR}/cmake/Modules/")



project (sparse_vector)

    # Trouver les bibliothèques et interpréteurs python par défaut
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs REQUIRED)
    message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
    message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
    message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
    message(STATUS "WARNING: Try 'export CPLUS_INCLUDE_PATH=${PYTHON_INCLUDE_DIRS}' if Boost building fails")
    include(BuildBoost) # module personnalisé

    include_directories(${Boost_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})
    link_directories(${Boost_LIBRARY_DIR})

    # Génère et lie le module pylib
    add_library(sparse_vector SHARED sparse_vector.cpp)
    target_link_libraries(sparse_vector ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
    add_dependencies(sparse_vector Boost)

    # Ajuste le nom de la bibliothèque pour coller à ce qu'attend Python
    set_target_properties(sparse_vector PROPERTIES SUFFIX .so)
    set_target_properties(sparse_vector PROPERTIES PREFIX "")

    # run test suite
    add_custom_target(test COMMAND python ../test_sparse_vector.py)
