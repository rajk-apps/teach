from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import requests
import json


class HelloWorldHandler(IPythonHandler):
    def get(self):
        resp = requests.get('http://localhost:6969/teach/status')
        self.write(json.dumps(resp.content.decode('utf-8')))
        self.finish()

    def post(self):
        code = self.get_argument('code')
        print(code)
        resp = requests.get('http://localhost:6969/teach/status',
                            params={'code': code})

        self.write(json.dumps(resp.content.decode('utf-8')))
        self.finish()


def load_jupyter_server_extension(nb_app):
    '''
    Register a hello world handler.

    Based on https://github.com/Carreau/jupyter-book/blob/master/extensions/server_ext.py
    '''
    web_app = nb_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/teach_status')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
