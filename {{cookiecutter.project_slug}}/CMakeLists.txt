cmake_minimum_required(VERSION 3.24)

project({{cookiecutter.project_slug}}
  VERSION 0.1.0
  LANGUAGES CXX
)

# ---------- default build type (single-config generators) ----------
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "{{cookiecutter.default_build_type}}" CACHE STRING "Build type" FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS Debug Release RelWithDebInfo MinSizeRel)
endif()

# ---------- options ----------
option({{cookiecutter.project_slug | upper}}_WARNINGS_AS_ERRORS "Treat warnings as errors" {% if cookiecutter.warnings_as_errors == "y" %}ON{% else %}OFF{% endif %})
option({{cookiecutter.project_slug | upper}}_USE_SANITIZERS "Enable ASan/UBSan on supported compilers" {% if cookiecutter.use_sanitizers == "y" %}ON{% else %}OFF{% endif %})
option({{cookiecutter.project_slug | upper}}_ENABLE_TESTS "Build tests" {% if cookiecutter.use_tests == "y" %}ON{% else %}OFF{% endif %})

# ---------- C++ standard ----------
set(CMAKE_CXX_STANDARD {{cookiecutter.cpp_standard}})
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ---------- export compile_commands.json (clang tools) ----------
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ---------- clang-tidy ----------
{% if cookiecutter.use_clang_tidy == "y" -%}
find_program(CLANG_TIDY_EXE NAMES clang-tidy)
if(CLANG_TIDY_EXE)
  message(STATUS "clang-tidy found: ${CLANG_TIDY_EXE}")
  set(CMAKE_CXX_CLANG_TIDY "${CLANG_TIDY_EXE}")
else()
  message(WARNING "clang-tidy requested but not found")
endif()
{% endif %}

# ---------- common warnings (as INTERFACE target) ----------
add_library({{cookiecutter.project_slug}}_warnings INTERFACE)

if(MSVC)
  target_compile_options({{cookiecutter.project_slug}}_warnings INTERFACE
    /W4
    /permissive-
  )
  if({{cookiecutter.project_slug | upper}}_WARNINGS_AS_ERRORS)
    target_compile_options({{cookiecutter.project_slug}}_warnings INTERFACE /WX)
  endif()
else()
  target_compile_options({{cookiecutter.project_slug}}_warnings INTERFACE
    -Wall -Wextra -Wpedantic
  )
  if({{cookiecutter.project_slug | upper}}_WARNINGS_AS_ERRORS)
    target_compile_options({{cookiecutter.project_slug}}_warnings INTERFACE -Werror)
  endif()
endif()

# ---------- sanitizers (as INTERFACE target) ----------
add_library({{cookiecutter.project_slug}}_sanitizers INTERFACE)
if({{cookiecutter.project_slug | upper}}_USE_SANITIZERS)
  if(NOT MSVC)
    target_compile_options({{cookiecutter.project_slug}}_sanitizers INTERFACE
      $<$<CONFIG:Debug>:-fsanitize=address,undefined>
      $<$<CONFIG:RelWithDebInfo>:-fsanitize=address,undefined>
    )
    target_link_options({{cookiecutter.project_slug}}_sanitizers INTERFACE
      $<$<CONFIG:Debug>:-fsanitize=address,undefined>
      $<$<CONFIG:RelWithDebInfo>:-fsanitize=address,undefined>
    )
  else()
    message(WARNING "Sanitizers are not enabled for MSVC in this template")
  endif()
endif()

# ---------- main targets ----------
add_subdirectory(src)

# ---------- tests ----------
if({{cookiecutter.project_slug | upper}}_ENABLE_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

# ---------- install / package (optional) ----------
{% if cookiecutter.use_package_init == "y" -%}
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Expect a library target named {{cookiecutter.project_slug}}::{{cookiecutter.project_slug}} from src/
# (We create it in src/CMakeLists.txt)
set(_pkg {{cookiecutter.project_slug}})

install(
  TARGETS {{cookiecutter.project_slug}}_lib
  EXPORT ${_pkg}Targets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
  EXPORT ${_pkg}Targets
  NAMESPACE ${_pkg}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${_pkg}
)

# Config + version files
set(config_in  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/{{cookiecutter.project_slug}}Config.cmake.in")
set(config_out "${CMAKE_CURRENT_BINARY_DIR}/{{cookiecutter.project_slug}}Config.cmake")
set(version_out "${CMAKE_CURRENT_BINARY_DIR}/{{cookiecutter.project_slug}}ConfigVersion.cmake")

configure_package_config_file(
  "${config_in}" "${config_out}"
  INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${_pkg}"
)

write_basic_package_version_file(
  "${version_out}"
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)

install(FILES "${config_out}" "${version_out}"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${_pkg}"
)
{% endif %}
