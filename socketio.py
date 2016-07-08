from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO
from threading import Thread
from logger import MyLogger
logger = MyLogger('client').init_logger('SIC', False, True)

Namespace = '/test'
class Main(LoggingNamespace):
    _connected = True

    def initialize(self):
        pass

class TestClient(Main):

    def on_disconnect(self):
        self.disconnect()

class socketIOClient(object):
    def __init__(self):
        self._server_ip = 'localhost'
        self._server_port = 5000
        self.socketio = None

    def onConnect(self):
        logger.info("From Server: onConnect")

    def onDisconnect(self):
        logger.info("From Server: onDisconnect")

    def onReconnect(self):
        logger.info("From Server: onReconnect")

    def connect(self):
        logger.info("Connecting ...")
        try:
            self.socketio = SocketIO(self._server_ip, self._server_port, Main)
            self.socketio_namespace = self.socketio.define(TestClient, Namespace)
        except Exception, e:
            logger.error("connect() except {0}".format(e))
            return

        try:
            self.socketio_namespace.on('connect', self.onConnect)
            self.socketio_namespace.on('disconnect', self.onDisconnect)
            self.socketio_namespace.on('reconnect', self.onReconnect)
            logger.info("socketio.on() success")
        except Exception, e:
            logger.error("socketio.on() except {0}".format(e))

        try:
            self.socketio.wait(seconds=1)
        except Exception, e:
            logger.error("wait() except {0}".format(e))

        logger.info("Connected.")

    def _async_emit(self, event, data={'data': 0}):
        try:
            self.connect()
            if self.socketio:
                self.socketio_namespace.emit(event, data)
                self.disconnect()
        except Exception, e:
            logger.error("_async_emit() except {0}".format(e))

    def emit(self, event, data={'data': 0}):
        logger.info("emit to server: {} - {}".format(event, str(data)))
        try:
            Thread(target=self._async_emit, args=(event,),
                   kwargs={'data': data}, name='thread_async_emit').start()
        except Exception, e:
            logger.error("emit() except {0}".format(e))

    def disconnect(self):
        try:
            logger.info("Disconnecting ...")
            if self.socketio:
                self.socketio.disconnect()

            logger.info("Disconnected.")
        except Exception, e:
            logger.error("disconnect() except {0}".format(e))

if __name__ == "__main__":
    # data = {'data': 'python client'}
    # socketIOClient().emit('my event', data)
    data = {'data': 'python client broadcast'}
    socketIOClient().emit('my broadcast event', data)
