from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    redis_rag_config_file_arg = DeclareLaunchArgument(
        'redis_rag_config',
        default_value=PathJoinSubstitution([FindPackageShare('fbot_db'), 'config', 'redis_rag.yaml']),
        description='Path to the redis_rag parameter file'
    )

    redis_rag_injector_node = Node(
        name='redis_rag_injector_node', 
        package='fbot_db', 
        executable='redis_rag_injector_node',
        parameters=[LaunchConfiguration('redis_rag_config'),
                    ]
    )

    return LaunchDescription([
        redis_rag_config_file_arg,
        redis_rag_injector_node,
    ])