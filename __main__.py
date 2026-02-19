import bottle
import os

__author__ = 'Luis Carrillo Gutiérrez'
__copyright__ = "Copyright 07/2020, Luis Carrillo Gutiérrez"
__desc__ = 'Proof of Concept of Recipe Book'

app = bottle.Bottle()

DB = '/tmp/data.db'
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MINIMAL_CORS = {
	'Content-type':'application/json',
	'Access-Control-Allow-Origin':'*',
	'Access-Control-Allow-Methods':'GET, POST, OPTIONS, PATCH, DELETE',
	'Access-Control-Allow-Headers':'*'
}

import Recipe

@app.error(404)
def errore404(error):
	return bottle.HTTPResponse(body={}, status=404)

@app.route('/', method='GET')
def ui():
	return bottle.static_file('index.html', root=os.path.join(ROOT_DIR, 'static'))

@app.route("/static/js/<filepath:path>", method='GET')
def js(filepath):
	return bottle.static_file(filepath, root=os.path.join(ROOT_DIR, 'static/js'))

if __name__ == "__main__":
	from flup.server.fcgi import WSGIServer
	WSGIServer(app).run()
