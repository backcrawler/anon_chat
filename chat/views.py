import tornado.web
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

import asyncio

from .handlers import SignedWebSocketHandler
from .utils import PairedConnections, check_code_valid

WAIT_TIME = 0.1
THRESHHOLD_TIME = 10
ws_connections = set()
paired_conns = PairedConnections()


class IndexView(tornado.web.RequestHandler):
    async def get(self):
        await self.render("templates/index.html")


class AjaxHandler(tornado.web.RequestHandler):
    async def post(self):
        print(self.request.body)
        data = json_decode(self.request.body)
        code = data['code']
        if not check_code_valid(code):  # if invalid code
            raise tornado.web.HTTPError(410)
        if code in paired_conns.waiting or paired_conns.get(code):
            raise tornado.web.HTTPError(403)  # if this conn already exists
        paired_conns[code] = None
        for _ in range(int(THRESHHOLD_TIME//WAIT_TIME)):
            await asyncio.sleep(WAIT_TIME)
            pair = paired_conns[code]
            if pair:
                break
            pair = paired_conns.get_random_conn()
            if pair == code:
                continue
            paired_conns[code] = pair
            break
        else:
            raise tornado.web.HTTPError(400)
        resp = {'status': 'sucess'}
        self.write(resp)


class MainWebsocket(SignedWebSocketHandler):
    async def open(self, *args: str, **kwargs: str):
        self.err = False
        self.idn = self.request.path.strip('/')
        if self.idn not in paired_conns.waiting:
            self.err = True
            await self.close(code=403, reason="Already here")
        try:
            self.pair_idn = paired_conns[self.idn]
        except KeyError:
            await self.close(code=410, reason="No such connection")
        self.__class__.mapping[self.idn] = self
        paired_conns.waiting.remove(self.idn)
        for _ in range((int(THRESHHOLD_TIME//WAIT_TIME))):
            await asyncio.sleep(WAIT_TIME)
            self.pair = self.__class__.mapping.get(self.pair_idn)
            if self.pair:
                break
        else:
            await self.close(code=400, reason="Connection time exceeded")
        print("WS OPENED:", self.idn)
        print("CONNS:", paired_conns.waiting)

    async def on_message(self, message):
        print("MESSAGE GOT:", message)
        await self.pair.write_message(message)

    async def on_close(self) -> None:
        print("WS CLOSED:", self.idn)
        try:
            del self.__class__.mapping[self.idn]
        except KeyError as e:
            pass
        if not self.err:
            del paired_conns[self.idn]
        print("CONNS:", paired_conns.waiting)