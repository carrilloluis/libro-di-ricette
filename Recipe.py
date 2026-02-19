from __main__ import app, DB, MINIMAL_CORS
import sqlite3
import json
import bottle
import uuid
import re
from contextlib import closing

@app.route('/Recipe/v1/<idx:re:[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}>/', method='GET')
def get_recipe(idx:str):
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT LOWER([i]) AS id, COALESCE([a], '') AS nm FROM [vy] WHERE [i]=LOWER(?)", (idx, ))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Recipe/v1/', method='GET')
def show_recipe():
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT LOWER([i]) AS id, COALESCE([a], '') AS nm FROM [vy] WHERE (([z] & 1) = 1)")
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Recipe/v1/_/<page:int>/<items:int>/', method='GET')
def show_recipe_by_page(page, items):
	ds_ = {}
	offset_ = (page - 1) * items
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT LOWER([i]) AS id, COALESCE([a], '') AS nm, ([z] & 1) AS st FROM [vy] ORDER BY a DESC LIMIT ? OFFSET ?", (items, offset_))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Recipe/v1/', method='POST')
def save_recipe():
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for create [Recipe]'}), status=400)
	try:
		params_ = (str(uuid.uuid4()), r['ds_'], )
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("INSERT INTO [vy] VALUES (LOWER(?), ?, 7)", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=201, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Recipe/v1/-/title/<idx:re:[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}>/', method='PATCH')
def update_recipe_title(idx):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Recipe title UPDATE]'}), status=400)
	try:
		params_ = (r['ds_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [vy] SET a=? WHERE i=LOWER(?) AND (z & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Recipe/v1/<idx:re:[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}>/', method='DELETE')
def disable_recipe(idx:str):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Recipe title DELETE]'}), status=400)
	try:
		params_ = (idx, )
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [vy] SET z=6 WHERE i=LOWER(?) AND (z & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)
