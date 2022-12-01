
if(NOT DEFINED PYTHON_DIR)
    get_filename_component(PYTHON_DIR ${CMAKE_CURRENT_LIST_DIR}/../../../../.venv ABSOLUTE)
endif()

if(NOT EXISTS ${PYTHON_DIR})
    message(FATAL_ERROR "Must create Python virtual envioronment at ${PYTHON_DIR}, e.g.: python3 -m venv .venv, OR define the cmake variable: PYTHON_DIR to point to the python directory")
endif()
message(STATUS "Using Python venv: ${PYTHON_DIR}")

set(Python3_FIND_VIRTUALENV ONLY)
set(Python3_FIND_STRATEGY LOCATION)
set(Python3_FIND_REGISTRY NEVER)
set(Python3_ROOT_DIR "${PYTHON_DIR}")
set(ENV{VIRTUAL_ENV} "${PYTHON_DIR}")
unset(Python3_FOUND) # Ensure Python is found again
unset(Python3_Interpreter_FOUND)
unset(Python3_EXECUTABLE)

find_package(Python3 REQUIRED)

message(STATUS "Python executable: ${Python3_EXECUTABLE}")
set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE} CACHE INTERNAL "Python executable path")


# Let pybind re-find python
# The cached variable: PYTHON_EXECUTABLE
# should already be defined so pybind11 should just use that
set(Python_FOUND OFF)
set(Python3_FOUND OFF)
set(Python3_FOUND OFF)


CPMAddPackage(
    NAME pybind11
    GITHUB_REPOSITORY pybind/pybind11
    GIT_TAG v2.6.2
    CACHE_VERSION v2.6.2
    CACHE_SUBDIR wrapper
)
