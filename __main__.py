import bottle
import os

__author__ = 'Luis Carrillo Gutiérrez'
__copyright__ = "Copyright 07/2020, Luis Carrillo Gutiérrez"
__desc__ = 'Proof of Concept'

app = bottle.Bottle()

DB = '/tmp/data.db'

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
	return 'Recipes - Local first?'

if __name__ == "__main__":
	from flup.server.fcgi import WSGIServer
	WSGIServer(app).run()