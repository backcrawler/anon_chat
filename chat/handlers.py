from tornado.websocket import WebSocketHandler


class SignedWebSocketHandler(WebSocketHandler):
    mapping = dict()