from launch_ros.actions import Node
from launch import LaunchDescription

def generate_launch_description():
    bayes_filter_node = Node(
        package='bayesian_estimation',
        executable='bayesian_estimation',
        name='bayes_filter_node',
        output='screen',
        parameters=[
            {"show_plot": True},
            {"plot_rate": 1.0}
        ]
    )

    return LaunchDescription([
        bayes_filter_node
    ])