from __main__ import app, DB, MINIMAL_CORS
import sqlite3
import json
import bottle
from contextlib import closing

@app.route('/Ingredient/v1/<idx:int>/', method='GET')
def get_ingredient(idx:int):
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT [i] AS id, LOWER([a]) AS rp, [b] AS qt, COALESCE([c], '') AS ut, COALESCE([d], '') AS nm, ([z] & 1) AS st FROM [xy] WHERE [i]=?", (idx, ))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Ingredient/v1/<idx:re:[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}>/', method='GET')
def show_ingredients_by_recipe(idx:str):
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT [i] AS id, [b] AS qt, COALESCE([c], '') AS ut, COALESCE([d], '') AS nm FROM [xy] WHERE LOWER([a])=? AND ([z] & 1)=1", (idx, ))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Ingredient/v1/', method='POST')
def save_ingredient():
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for create [Ingredient]'}), status=400)
	try:
		params_ = (r['rp_'], float(r['qt_']), r['ut_'], r['nm_'], )
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("INSERT INTO [xy] VALUES (NULL, ?, ?, ?, ?, 7)", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=201, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Ingredient/v1/<idx:int>/', method='DELETE')
def disable_ingredient(idx):
	try:
		params_ = (r['ds_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [xy] SET [z]=6 WHERE [i]=? AND ([z] & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Ingredient/v1/-/quantity/<idx:int>/', method='PATCH')
def update_ingredient_quantity(idx):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Ingredient quantity UPDATE]'}), status=400)
	try:
		params_ = (r['qt_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [xy] SET [b]=? WHERE [i]=? AND ([z] & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Ingredient/v1/-/unit/<idx:int>/', method='PATCH')
def update_ingredient_unit(idx):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Ingredient unit UPDATE]'}), status=400)
	try:
		params_ = (r['ut_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [xy] SET [c]=? WHERE [i]=? AND ([z] & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Ingredient/v1/-/title/<idx:int>/', method='PATCH')
def update_ingredient_desc(idx):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Ingredient description UPDATE]'}), status=400)
	try:
		params_ = (r['nm_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [xy] SET [d]=? WHERE [i]=? AND ([z] & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)
