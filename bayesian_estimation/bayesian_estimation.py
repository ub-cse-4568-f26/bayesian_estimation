import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import numpy as np
import time

class BayesFilter(Node):
    def __init__(self):
        super().__init__('bayes_filter_node')
        
        self.belief = np.zeros((20, 20))  # initial belief
        self.belief[10][10] = 1  # We know our initial position with 100% certainity

        self.action_probs = None
        self.obs_probs = None

        self.declare_parameter("show_plot", True)
        self.showPlot = self.get_parameter("show_plot").get_parameter_value().bool_value
        self.declare_parameter("plot_rate", 1.0)
        self.plotRate = self.get_parameter("plot_rate").get_parameter_value().double_value

        self.updateSub = self.create_subscription(
            String,
            "robot",
            self.estimationCb,
            1
        )

        self.beliefPub = self.create_publisher(
            Float32MultiArray,
            "belief",
            1
        )

        self.plt_update_timer = self.create_timer(1.0/self.plotRate, self.update_plot)

        if self.showPlot:
            plt.ion()
            plt.rcParams["grid.color"] = (0.5, 0.5, 0.5, 0.1)
            self.fig = plt.figure()
            self.update_plot()

    def estimationCb(self, msg: String):
        cmd_list = str.split(msg.data, " ")

        if self.action_probs is None or self.obs_probs is None:
            self.get_logger().info("Please setup models first.")
            return

        for cmd in cmd_list:
            if (
                cmd[0].capitalize() == "R"
                or cmd[0].capitalize() == "L"
                or cmd[0].capitalize() == "U"
                or cmd[0].capitalize() == "D"
            ):
                self.get_logger().info(f"Got Action: {cmd.capitalize()}")
                steps = int(cmd[1:])
                for _ in range(steps):
                    self.belief = self.action_update(cmd[0].capitalize())
                    self.update_plot()
                    time.sleep(1/self.plotRate)
            elif cmd[0].capitalize() == "X" or cmd[0].capitalize() == "Y":
                self.get_logger().info(f"Got Observation: {cmd.capitalize()}")
                self.belief = self.observation_update(cmd.capitalize())
                self.update_plot()
                time.sleep(1/self.plotRate)
            else:
                self.get_logger().info("Invalid input received.")
                continue

    def update_plot(self):
        if self.showPlot:
            try:
                for ax in self.fig.axes:
                    if ax.get_label() == "<colorbar>":
                        self.fig.delaxes(ax)
                self.fig.clear()
            except:
                pass
    
            plt.title("Robot Belief Model")
            plt.imshow(self.belief, origin="lower")
            plt.xticks(np.arange(0, 20, 5))
            plt.yticks(np.arange(0, 20, 5))
            plt.minorticks_on()
            minor_ticks = np.arange(0.5, 20.5, 1)
            plt.gca().xaxis.set_minor_locator(FixedLocator(minor_ticks))
            plt.gca().yaxis.set_minor_locator(FixedLocator(minor_ticks))
            plt.grid(True, which='minor', color='gray', linewidth=0.5, alpha=0.3)
            try:
                plt.colorbar()
            except:
                pass
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        msg = Float32MultiArray()
        msg.data = self.belief.flatten().astype(float).tolist()
        self.beliefPub.publish(msg)

    """
        DO NOT CHANGE ANYTING ABOVE THIS LINE

        TO-DO: Implement the following functions to complete the Bayes Filter        
    """

    def setupModels(self):
        # Initialize the arrays for action and observation probabilities
        self.action_probs = None
        self.obs_probs = None


    def action_update(self, motion):
        '''
        Args:
        motion: string of direction of action. Can only be 'U', 'D', 'L', 'R'
        
        Function estimationCb() in this file calls this function when it receives an action command n times. Uses the current belief (self.belief) and the action to compute the new belief.
        
        Returns:
        new_belief: numpy array of new belief after action update
        '''
        new_belief = np.zeros(self.belief.shape)

        # Compute new belief and return based on current "motion" and current belief from self.belief
        # Task 1: ===============================================

        # Perform the action update here

          
        # ========================================================
        
        # Normalize the belief



        return new_belief

    def observation_update(self, obs):
        '''
        Args:
        obs: string of observation. Is of the form 'Xn' or 'Yn' where n is index of the observation. X10 means that the sensor thinks that all X values with index 10 are likely to be true. Y5 would mean that all Y values with index 5 are likely to be true.
        
        Function estimationCb() in this file calls this function when it receives an observation command. Uses the current belief (self.belief) and the observation to compute the new belief.
        
        Returns:
        new_belief: numpy array of new belief after sensor update
        '''
        new_belief = np.zeros(self.belief.shape)

        # Compute belief and return based on current "obs" and current belief from self.belief
        # Task 2: ===============================================

        # Perform the sensor update here

        
        # ========================================================
        
        # Normalize the belief

        return new_belief

def main():
    rclpy.init()
    node = BayesFilter()
    node.setupModels()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
