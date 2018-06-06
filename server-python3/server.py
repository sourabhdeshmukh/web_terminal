import os
import config
import urllib.parse
import eventlet
import eventlet.green.socket
import eventlet.websocket
import eventlet.wsgi
import wspty.pipe
from flask import Flask, request, redirect
from wspty.EncodedTerminal import EncodedTerminal
from wspty.WebsocketBinding import WebsocketBinding


def make_app():
    app = Flask(__name__)
    app.static_folder = get_static_folder()

    @app.route('/')
    def index():
        newurl = b'/static/index.html'
        if request.query_string:
            newurl = newurl + b'?' + request.query_string
        return redirect(newurl)
    return app

def parse_query(qstr):
    return {k: v[0] for k, v in urllib.parse.parse_qs(qstr).items()}

def debug(s):
    app.logger.debug(s)


class TerminalFactory:
    def __init__(self, args_dict, allow_unsafe=False):
        self.encoding = args_dict.get('encoding', 'utf8')
        self.allow_unsafe = allow_unsafe

    def create_binary(self):
        from wspty import PromptTerminal
        return PromptTerminal.os_terminal()
        
    def create(self):
        return EncodedTerminal(self.create_binary(), self.encoding)


class DefaultRootApp:
    def __init__(self):
        self._app_handle_wssh = eventlet.websocket.WebSocketWSGI(self.handle_wssh)
        self.allow_unsafe = True

    def handle_wssh(self, ws):
        debug('Creating terminal with remote {remote}'.format(
            remote=ws.environ.get('REMOTE_ADDR'),
        ))
        ws_binding = WebsocketBinding(ws)
        query = parse_query(ws.environ.get('QUERY_STRING', ''))
        terminal = None
        terminal = self.create_terminal(query)
        wspty.pipe.pipe(ws_binding, terminal)
        debug('Closing terminal normally with remote {remote}'.format(
            remote=ws.environ.get('REMOTE_ADDR'),
        ))
        return ''

    def create_terminal(self, obj):
        factory = TerminalFactory(obj, self.allow_unsafe)
        return factory.create()

    def handler(self, env, *args):
        route = env["PATH_INFO"]
        if route == '/wssh':
            return self._app_handle_wssh(env, *args)
        else:
            return app(env, *args)


def make_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Websocket Terminal server')
    parser.add_argument('-l', '--listen', default='', help='Listen on interface (default all)')
    parser.add_argument('-p', '--port', default=5002, type=int, help='Listen on port')
    parser.add_argument('--unsafe', action='store_true', help='Allow unauthenticated connections to local machine')
    return parser

def start(interface, port, root_app_handler):
    conn = (interface, port)
    listener = eventlet.listen(conn)
    print('listening on {0}:{1}'.format(*conn))
    try:
        eventlet.wsgi.server(listener, root_app_handler)
    except KeyboardInterrupt:
        pass

def start_default(interface, port, root_app_cls=DefaultRootApp):
    root_app = root_app_cls()
    start(interface, port, root_app.handler)


def main():
    args = make_parser().parse_args()
    start_default(args.listen, args.port)


def get_static_folder():
    path_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../client')
    path_root = os.path.join(path_root, config.CLIENT_DIR)
    return os.path.abspath(path_root)


app = make_app()

if __name__ == '__main__':
    main()
    
