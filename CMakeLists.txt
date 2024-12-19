cmake_minimum_required(VERSION 3.8)
project(fbot_db)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED) 
find_package(geometry_msgs REQUIRED)
find_package(vision_msgs REQUIRED)
find_package(fbot_vision_msgs REQUIRED)


# Custom interfaces
rosidl_generate_interfaces(${PROJECT_NAME} 
  "srv/RedisCacheReaderSrv.srv"
  "srv/RedisCacheWriterSrv.srv"
  "srv/RedisRagInjectorSrv.srv"
  "srv/RedisRagRetrieverSrv.srv"
  DEPENDENCIES std_msgs fbot_vision_msgs
)


install(DIRECTORY src/${PROJECT_NAME}/plugins
  DESTINATION lib/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.py"

)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
