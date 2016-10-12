import zmq


class Client():
    """This class represents test-harness client.

    The client helps in sending/receiving the requests to the
    <your-ZeroMQ-application-name> server. The requests are made
    by using the tests defined in definitions.py.

    Attributes:
        protocol (str): The protocol either of tcp, udp, pgm, epgm, inproc, ipc
        interface (str): The network interface
        port (TestType): The port number
        socketType (int): The type of socket
        _context (list): The zmq context object
        _socket (dict): The zmq socket object
    """

    def __init__(self, protocol, interface, port, socketType):
        self.protocol = protocol
        self.interface = interface
        self.port = port
        self.socketType = socketType
        self._context = None
        self._socket = None

    def connect(self):
        """This method connects the client to the server."""

        self._context = zmq.Context()
        self._socket = self._context.socket(self.socketType)

        # The client must know the server's public key to make a CURVE connection.
        # FIXME: These should not be hardcoded; you should change this by moving
        #        these ta a certificate directory and reading them from there
        self._socket.curve_secretkey = "pJ9TH5i:.<13*2aM:nx}Es83SRyaPD?rD$Sb@0&7"
        self._socket.curve_publickey = "qT>h?AgefUrapaz83<Z6K)S{0sB)?VH:6P#!72vi"
        self._socket.curve_serverkey = "9x:/U@Ypd+1l@&H1Te{exRPUO.i:(S+/WH.Stv3T"

        # Connect the client
        self._socket.connect("%s://%s:%s" % (self.protocol, self.interface, self.port))

    def disconnect(self):
        """This method disconnects the client from the server."""

        self._socket.disconnect("%s://%s:%s" % (self.protocol, self.interface, self.port))

    def sendData(self, inData):
        """This method sends the data to the server.

        Args:
            inData (str): The input data to be send to the server.
        """

        try:
            self._socket.send(inData)
        except zmq.ZMQError, e:
            print "Error: send did not succeed for some reason:", e

    def receiveData(self):
        """This method receives the data from the server.

        Returns:
            The received data from the server.
        """

        try:
            messageFromServer = self._socket.recv()
            return messageFromServer
        except zmq.ZMQError, e:
            print "Error: recv did not succeed for some reason:", e
