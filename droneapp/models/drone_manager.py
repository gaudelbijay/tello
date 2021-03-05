import logging
import socket
import sys
import threading
import time

logging.basicConfig(level=logging.INFO, steam=sys.stdout)
logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 0.30
DEFAULT_SPEED = 10
DEFAULT_DEGREE = 10


class DroneManager(object):
    def __init__(self, host_ip='192.168.1.70', host_port=8889, drone_ip='192.168.10.1', drone_port=8889,
                 is_imperial=False, speed=10):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.is_imperial = is_imperial
        self.speed = speed

        self.drone_address = (drone_ip, drone_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.host_ip, self.host_port)
        self.send_command(b'command', self.drone_address)  # To activate tello sdk
        self.send_command(b'streamon', self.drone_address)

        self.response = None
        self.stop_event = threading.Event()

        self._response_thread = threading.Thread(target=self.receive_response, args=(self.stop_event,))
        self._response_thread.start()

        self.set_speed(self.speed)

    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(1024)
                logger.info({'action': 'receive_respone', 'response': self.response})
            except socket.error as ex:
                logger.error({'action': 'recieve_response', 'ex': ex})
                break

    def __dell__(self, ):
        self.stop()

    def stop(self, retry=0):
        self.stop_event.set()

        while self._response_thread.isAlive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry += 1

        self.socket.close()

    def send_command(self, command, retry=0):
        logger.info({'action': 'send_command', 'command': command})

        self.socket.sendto(command.encode('utf-8'), self.drone_address)

        while self.response is None:
            time.sleep(0.3)

            if retry > 5:
                break
            retry += 1

        if self.response is None:
            response = None
        else:
            response = self.response.decode('utf-8')

        self.response = None

        return response

    def takeoff(self, ):
        self.send_command('takeoff')

    def land(self, ):
        self.send_command('land')

    def move(self, direction, distance):
        distance = float(distance)
        if self.is_imperial:
            distance = int(round(distance * 30.481))
        else:
            distance = int(round(distance * 100))
        return self.send_command(f'{direction}{distance}')

    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)

    def down(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)

    def right(self, distance=DEFAULT_DISTANCE):
        return self.move('right', distance)

    def left(self, distance=DEFAULT_DISTANCE):
        return self.move('left', distance)

    def forward(self, distance=DEFAULT_DISTANCE):
        return self.move('forward', distance)

    def back(self, distance=DEFAULT_DISTANCE):
        return self.move('back', distance)

    def set_speed(self, speed):
        return self.send_command(f'speed {speed}')

    def clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'cw {degree}')

    def counter_clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'ccw {degree}')

    def flip(self, direction='l'):
        return self.send_command(f'flip {direction}')


if __name__ == '__main__':
    drone_manager = DroneManager()
    drone_manager.takeoff()
    time.sleep(20)
    drone_manager.land()
