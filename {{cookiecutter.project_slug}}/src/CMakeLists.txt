# Library/executable layout:
# - If use_package_init == y: build a library + an example executable (main.cpp)
# - Otherwise: build only an executable (main.cpp)

{% if cookiecutter.use_package_init == "y" -%}
add_library({{cookiecutter.project_slug}}_lib)
add_library({{cookiecutter.project_slug}}::{{cookiecutter.project_slug}} ALIAS {{cookiecutter.project_slug}}_lib)

target_sources({{cookiecutter.project_slug}}_lib
  PRIVATE
    # Put your library sources here (create as needed)
    # e.g. ${CMAKE_CURRENT_SOURCE_DIR}/foo.cpp
)

target_include_directories({{cookiecutter.project_slug}}_lib
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries({{cookiecutter.project_slug}}_lib
  PUBLIC
    {{cookiecutter.project_slug}}_warnings
    {{cookiecutter.project_slug}}_sanitizers
)

# Example executable
add_executable({{cookiecutter.project_slug}} main.cpp)
target_link_libraries({{cookiecutter.project_slug}}
  PRIVATE
    {{cookiecutter.project_slug}}::{{cookiecutter.project_slug}}
)

{% else -%}

add_executable({{cookiecutter.project_slug}} main.cpp)

target_include_directories({{cookiecutter.project_slug}}
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

target_link_libraries({{cookiecutter.project_slug}}
  PRIVATE
    {{cookiecutter.project_slug}}_warnings
    {{cookiecutter.project_slug}}_sanitizers
)

{% endif %}
