from chat.app import run_server

import datetime
import logging

if __name__ == '__main__':
    print('SERVER STARTED: ', datetime.datetime.today().ctime())
    run_server()