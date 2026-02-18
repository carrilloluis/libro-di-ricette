from __main__ import app, DB, MINIMAL_CORS
import sqlite3
import json
import bottle
from contextlib import closing

@app.route('/Recipe/v1/<idx:int>/', method='GET')
def get_recipe(idx:int):
	ds_ = {}
	str_retrieve = """
		SELECT [i] AS id, COALESCE([a], '') AS nm FROM [vy] 
		WHERE [i]=?
		"""
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute(str_retrieve, (idx, ))
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
	str_list = """
		SELECT [i] AS id, COALESCE([a], '') AS nm FROM [vy] 
		WHERE (([z] & 1) = 1)
		"""
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute(str_list)
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
	str_paging = """
		SELECT [i] AS id, COALESCE([a], '') AS nm, ([z] & 1) AS st FROM [vy] 
		ORDER BY a DESC LIMIT ? OFFSET ?
		"""
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute(str_paging, (items, offset_))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Recipe/v1/', method='POST')
def save_recipe():
	str_insert = "INSERT INTO [vy] VALUES (NULL, ?, 7)"
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for create [Recipe]'}), status=400)
	try:
		params_ = (r['ds_'], )
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute(str_insert, params_)
				connection_.commit()
				return bottle.HTTPResponse(status=201, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Recipe/v1/-/title/<idx:int>/', method='PATCH')
def update_recipe_title(idx):
	str_update_title = "UPDATE [vy] SET a=? WHERE i=? AND (z & 1) = 1"
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Recipe title UPDATE]'}), status=400)
	try:
		params_ = (r['ds_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute(str_update_title, params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS) # body={},
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)