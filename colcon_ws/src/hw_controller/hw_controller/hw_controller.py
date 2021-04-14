#ROS 2 related imports:
import rclpy
from rclpy.node import Node

#Message imports:
from hrp_msgs.msg import HrpMeasurementSensor
from std_msgs.msg import String

#Other imports:
import time
import serial

class hwController(Node):

    def __init__(self):
        super().__init__('hw_controller')

        #namespace paths
        self.hrp1 = '/hrp/hrp1/'
        self.ga1 = '/ga/ga1/'
        self.ga_s1 = '/ga_s/ga_s1/'
        self.light1 = 'light/light1/'

        #command and state decoding mapping dictionaries

        self.colorCmdDict = {
            "off"   :   0 << 2,
            "red"   :   1 << 2,
            "blue"  :   2 << 2,
            "green" :   3 << 2,
            "yellow":   4 << 2,
            "white" :   5 << 2,
        }

        # decode does not need bit shifting and off is discarded
        self.colorDecodeDict = {
            1 : "red",
            2 : "blue",
            3 : "green",
            4 : "yellow",
            5 : "white",
        }

        self.actuatorCmdDict = {
            "coast" :   0,
            "up"    :   1,
            "down"  :   2,  
        }

        # coast is not SP state and is discarded
        self.actuatorDecodeDict = {
            1 : "up",
            2 : "down",
        }

        self.trashSensorDecodeDict = {
            1 : "on",
            0 : "off",
        }

        self.parsedStateDict = dict.fromkeys(['R', 'L', 'F', 'A' ,'T' ,'I'])

        #variable defenitions
        self.currentColorCmd = self.colorCmdDict["blue"]    # holds current command byte for color
        self.currentActuatorCmd = 0                         # holds current actuator command

        #init of serial com:
        self.ser = self.initSerial()

        #check if serial port is open
        if(self.ser.isOpen()):
            self.get_logger().info("Serial port opened")


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
        self.ga1+'controller_state',
        10)

        self.indicatorLightStatePub = self.create_publisher(
        String,
        self.light1+'controller_state',
        10)

        #defining subscribers:

        self.trashActuatorGoalSub = self.create_subscription(
        String,
        self.ga1+'controller_goal',
        self.trashActuatorGoalSubCallback,
        10)

        self.indicatorLightGoalSub = self.create_subscription(
        String,
        self.light1+'controller_goal',
        self.indicatorLightGoalSubCallback,
        10)


        #define timer for serial read
        timer_period = 0.1
        self.timerSerial = self.create_timer(timer_period, self.serialTimerCallback)

    #defining timer callbacks
    
    def serialTimerCallback(self):
        # Check if data is available to read (https://stackoverflow.com/questions/38645060/what-is-the-equivalent-of-serial-available-in-pyserial)
        if self.ser.in_waiting > 0:
            #find start of packet:
            while(self.ser.readline().decode("utf-8") !=  "PACKET:\n"):
                pass
            for _x in range(0, len(self.parsedStateDict)):
                try:
                    line = self.ser.readline().decode("utf-8")
                    [stateType, state] = line.split(": ")
                except ValueError:
                    self.get_logger().warn("Decode or splitting of string failed")
                    return #skips this decode iteration - TODO look into better way to hande this

                if stateType in self.parsedStateDict.keys():
                    try:
                        self.parsedStateDict[stateType] = int(state.strip())
                    except ValueError:
                        self.get_logger().warn("String to int conversion failed!")
                else:
                    self.get_logger().error("INCORRECT SERIAL PARSE KEY")
            print(self.parsedStateDict)

            # publish values to ros topics:
            self.distSensorSend()
            self.trashSensorSend()
            self.trashActuatorStateSend()
            self.indicatorLightStateSend()


    #defining subscriber callbacks

    def indicatorLightGoalSubCallback(self, msg):
        if msg.data in self.colorCmdDict.keys():
            self.currentColorCmd = self.colorCmdDict[msg.data]
            self.sendSerialCommand()
        else:
            self.get_logger().error("Invalid color command: " + msg.data)

    def trashActuatorGoalSubCallback(self, msg):
        if msg.data in self.actuatorCmdDict.keys():
            self.currentActuatorCmd = self.actuatorCmdDict[msg.data]
            self.sendSerialCommand()
        else:
            self.get_logger().error("Invalid actuator command: " + msg.data)

    # defining publishing functions:

    def distSensorSend(self):
        msg = HrpMeasurementSensor()
        msg.f = self.parsedStateDict["F"]
        msg.l = self.parsedStateDict["L"]
        msg.r = self.parsedStateDict["R"]
        self.distSensorPub.publish(msg)

    def trashSensorSend(self):
        msg = String()
        msg.data = self.trashSensorDecodeDict[self.parsedStateDict["T"]]
        self.trashSensorPub.publish(msg)

    def trashActuatorStateSend(self):
        msg = String()
        # check key so we ignore off state (not a SP state)
        if self.parsedStateDict["A"] in self.actuatorDecodeDict.keys():
            msg.data = self.actuatorDecodeDict[self.parsedStateDict["A"]]
            self.trashActuatorStatePub.publish(msg)

    def indicatorLightStateSend(self):
        msg = String()
        # check key so we ignore off state (not a SP state)
        if self.parsedStateDict["I"] in self.colorDecodeDict.keys():
            msg.data = self.colorDecodeDict[self.parsedStateDict["I"]]
            self.indicatorLightStatePub.publish(msg)

    # defining helper functions

    def sendSerialCommand(self):
        # compose command via bitwise and:
        cmd = self.currentColorCmd | self.currentActuatorCmd
        self.get_logger().debug("Serial command: " + "{0:b}".format(cmd) ) 
        packet = bytearray()
        packet.append(cmd)
        self.ser.write(packet)

    def initSerial(self):
        #TODO: update to make these configurable arguments
        #TODO: add exception handling when the port fails to be configured
        # Serial port is instantly opened upon creation (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        ser = serial.Serial(
        port='/dev/ttyACM1',
        baudrate=115200,
        timeout = 3)
        return ser

    def closeSerial(self):
        self.ser.close()
        self.get_logger.info("Closing serial port")

def main(args=None):
    rclpy.init(args=args)

    controller = hwController()

    rclpy.spin(controller)

    #close the serial port before the node is destroyed:
    controller.closeSerial()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
