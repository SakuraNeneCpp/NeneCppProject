# Only built when {{cookiecutter.project_slug | upper}}_ENABLE_TESTS is ON

include(FetchContent)

set(TEST_TARGET {{cookiecutter.project_slug}}_tests)

{% if cookiecutter.test_framework == "Catch2" -%}
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.5.4
)
FetchContent_MakeAvailable(Catch2)

add_executable(${TEST_TARGET} test_main.cpp)
target_link_libraries(${TEST_TARGET}
  PRIVATE
    Catch2::Catch2WithMain
    {{cookiecutter.project_slug}}_warnings
    {{cookiecutter.project_slug}}_sanitizers
    {% if cookiecutter.use_package_init == "y" -%}
    {{cookiecutter.project_slug}}::{{cookiecutter.project_slug}}
    {% endif -%}
)

add_test(NAME ${TEST_TARGET} COMMAND ${TEST_TARGET})

{% elif cookiecutter.test_framework == "doctest" -%}
FetchContent_Declare(
  doctest
  GIT_REPOSITORY https://github.com/doctest/doctest.git
  GIT_TAG v2.4.11
)
FetchContent_MakeAvailable(doctest)

add_executable(${TEST_TARGET} test_main.cpp)
target_link_libraries(${TEST_TARGET}
  PRIVATE
    doctest::doctest
    {{cookiecutter.project_slug}}_warnings
    {{cookiecutter.project_slug}}_sanitizers
    {% if cookiecutter.use_package_init == "y" -%}
    {{cookiecutter.project_slug}}::{{cookiecutter.project_slug}}
    {% endif -%}
)

add_test(NAME ${TEST_TARGET} COMMAND ${TEST_TARGET})

{% else -%}
# Framework = none
message(STATUS "Tests enabled but no framework selected. Add your own test runner in tests/CMakeLists.txt.")
{% endif -%}
