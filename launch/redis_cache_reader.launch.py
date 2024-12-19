from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    redis_cache_config_file_arg = DeclareLaunchArgument(
        'redis_cache_config',
        default_value=PathJoinSubstitution([FindPackageShare('fbot_db'), 'config', 'redis_cache.yaml']),
        description='Path to the ros parameter file'
    )

    plugin_config_file_arg = DeclareLaunchArgument(
        'plugin_config',
        default_value=PathJoinSubstitution([FindPackageShare('fbot_db'), 'config', 'plugin.yaml']),
        description='Path to the plugin parameter file'
    )


    redis_cache_reader_node = Node(
        name='redis_cache_reader', 
        package='fbot_db', 
        executable='redis_cache_reader',
        parameters=[LaunchConfiguration('redis_cache_config'),
                    LaunchConfiguration('plugin_config'), 
                    ]
    )

    return LaunchDescription([
        redis_cache_config_file_arg,
        plugin_config_file_arg,
        redis_cache_reader_node,
    ])