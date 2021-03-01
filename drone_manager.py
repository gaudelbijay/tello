import logging
import socket
import sys
import threading
import time

logging.basicConfig(level=logging.INFO, steam=sys.stdout)
logger = logging.getLogger(__name__)


class DroneManager(object):
    def __init__(self, host_ip='192.168.1.70', host_port=8889, drone_ip='192.168.10.1', drone_port=8889):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.socket = socket.socket(socket.socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.host_ip, self.host_port)
        self.send_command(b'command', self.drone_address)  # To activate tello sdk
        self.send_command(b'streamon', self.drone_address)

        self.response = None
        self.stop_event = threading.Event()

        self._response_thread = threading.Thread(target=self.receive_response, args=(self.stop_event,))
        self._response_thread.start()

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

    def stop(self, retry):
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


if __name__ == '__main__':
    drone_manager = DroneManager()
    drone_manager.takeoff()

    time.sleep(20)

    drone_manager.land()
