#ROS 2 related imports:
import rclpy
from rclpy.node import Node

from hrp_msgs.msg import HrpMeasurementSensor
from std_msgs.msg import String

class hwController(Node):

    def __init__(self):
        super().__init__('hw_controller')

        #namespace paths:
        self.hrp1 = '/hrp/hrp1/'
        self.ga1 = '/ga/ga1/'
        self.ga_s1 = '/ga_s/ga_s1/'
        self.light = 'light/light_1/'

        #command mapping
        self.colorCmd = {
            "off"   :   0 << 2,
            "red"   :   1 << 2,
            "blue"  :   2 << 2,
            "green" :   3 << 2,
            "yellow":   4 << 2,
            "white" :   5 << 2,
        }
        # https://stackoverflow.com/questions/1456373/two-way-reverse-map
        self.reverseColorCmd = dict(reversed(item) for item in self.colorCmd.items())

        self.actuatorCmd = {
            "coast" :   0,
            "up"    :   1,
            "down"  :   2,  
        }
        #TODO add reverse dictionary here as well

        #defining publishers

        self.distSensorPub = self.create_publisher(
        HrpMeasurementSensor,
        self.hrp1+'unicorn_measurement_sensor',
        10)

        self.trashSensorPub = self.create_publisher(
        String,
        self.ga_s1+'controller_state',
        10)

        self.trashActuatorStatePub = self.create_publisher(
        String,
        self.ga+'controller_state',
        10)

        self.IndicatorLightStatePub = self.create_publisher(
        String,
        self.ga+'controller_state',
        10)

        #defining subscribers:

        self.trashActuatorStatePub = self.create_publisher(
        String,
        self.ga+'controller_state',
        10)

        self.IndicatorLightStatePub = self.create_publisher(
        String,
        self.ga+'controller_state',
        10)


        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = HrpMeasurementSensor()
        msg.f = 100
        msg.r = 100
        msg.l = 100
        self.publisher_.publish(msg)

def initSerial():
    #TODO: update to make these configurable arguments
    ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    timeout = 3
    )

def main(args=None):
    rclpy.init(args=args)

    controller = hwController()

    rclpy.spin(controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()