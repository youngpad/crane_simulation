# Ros imports
from xml.dom.expatbuilder import theDOMImplementation
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from math import pi, sin, cos

# Project imports
from crane_interfaces.msg import Reference


class Simulator(Node):
    def __init__(self):
        # Name node
        super().__init__('crane_simulator')

        # Joint state publisher
        joint_state_topic = "joint_states"
        self.joint_state_pub = self.create_publisher(JointState,
                                                     joint_state_topic,
                                                     10)

        # Reference subscriber
        reference_topic = "dundermifflin/scranton/msg"
        self.ref_sub = self.create_subscription(Reference, 
                                                reference_topic,
                                                self.ref_callback,
                                                10)

        # Node frequency setup
        self.frequency = 30
        self.loop_rate = self.create_rate(self.frequency)

        # Joint variables
        self.min_lim = -pi/8
        self.max_lim = pi/8
        self.alpha_boom = 0.1
        self.omega_boom = 0
        self.theta_boom = 0.0
        self.joint_state_msg = JointState()

        # Run simulation
        self.simulate()
        
    def ref_callback(self, msg):
        pass
    
    def simulate(self):
        try: 
            while rclpy.ok():
                # Spin node once
                rclpy.spin_once(self)

                # Get time
                now = self.get_clock().now()

                # Simulate
                time = now.nanoseconds * 1e-9
                self.omega_boom = 0.05*cos(0.2*time)
                self.theta_boom += self.omega_boom*(1/self.frequency)
                print(self.theta_boom)

                # Update joint state
                self.joint_state_msg.header.stamp = now.to_msg()
                self.joint_state_msg.name = ['base_to_crane_boom']
                self.joint_state_msg.position = [self.theta_boom] 

                # Publish
                self.joint_state_pub.publish(self.joint_state_msg)

                # Sleep
                self.loop_rate.sleep()
        except KeyboardInterrupt:
            pass

        
def main(args=None):
    rclpy.init(args=args)
    node = Simulator()
    #rclpy.spin(Simulator)
    #rclpy.shutdown()


if __name__ == '__main__':
    main()