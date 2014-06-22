__author__ = 'develru'


from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.python import log
import sys
from components import DriveModule


class DriveConnect(Protocol):

    def __init__(self):
        log.startLogging(sys.stdout)
        self.drive = DriveModule()

    def connectionMade(self):
        print('Connect')
        self.transport.write('Connected')

    def connectionLost(self, reason):
        print('Connection lost')
        self.drive.stop()
        self.drive.offline()

    def dataReceived(self, data):
        print('Data received')
        #data_str = data.decode(encoding='base64')
        print(data)

        if data == 'FW':
            print('Forward')
            self.drive.drive_forward()
        elif data == 'BW':
            print('Backward')
            self.drive.drive_backward()
        elif data == 'RT':
            print('Right')
            self.drive.steer_right()
        elif data == 'LT':
            print('Left')
            self.drive.steer_left()
        elif data == 'ST':
            print('Stop')
            self.drive.stop()
        elif data == 'DRVST':
            self.drive.online()
            self.transport.write('online')



class DriveFactory(Factory):

    def buildProtocol(self, addr):
        return DriveConnect()

#import socketserver

# class DriveTCPHandler(socketserver.StreamRequestHandler):
#
#     def handle(self):
#         self.data = self.rfile.readline().strip()
#         print('{} wrote'.format(self.client_address[0]))
#         print(self.data)
#         self.wfile.write(self.data.upper())


class MainHandler:

    def __init__(self, host, port=8080):
        self._host = host
        self._port = port

    def main_run(self):
        reactor.listenTCP(self._port, DriveFactory())
        reactor.run()


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999


    reactor.listenTCP(PORT, DriveFactory())
    reactor.run()

    #
    # server = socketserver.TCPServer((HOST, PORT), DriveTCPHandler)
    #
    # server.serve_forever()
