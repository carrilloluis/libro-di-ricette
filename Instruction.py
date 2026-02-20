from __main__ import app, DB, MINIMAL_CORS
import sqlite3
import json
import bottle
from contextlib import closing

@app.route('/Instruction/v1/<idx:int>/', method='GET')
def get_instruction_by_id(idx:int):
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT [i] AS id, COALESCE([a], '') AS rp, COALESCE([b], '') AS nm, ([z] & 1) AS st FROM [yz] WHERE [i]=?", (idx, ))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Instruction/v1/<idx:re:[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}>/', method='GET')
def show_instructions_per_recipe(idx:str):
	ds_ = {}
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.row_factory = sqlite3.Row
				cursor_.execute("SELECT [i] AS id, COALESCE([b], '') AS nm FROM [yz] WHERE [a]=LOWER(?) AND ([z] & 1)=1", (idx, ))
				ds_ = [dict(r) for r in cursor_.fetchall()]
	except sqlite3.OperationalError as e1:
		return bottle.HTTPResponse(body=json.dumps({'error' : str(e1) }), status=500)
	if len(ds_) > 0:
		return bottle.HTTPResponse(body=json.dumps(ds_), status=200, headers=MINIMAL_CORS)
	else:
		return bottle.HTTPResponse(body={}, status=404)

@app.route('/Instruction/v1/', method='POST')
def save_instruction():
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for create [Instruction]'}), status=400)
	try:
		params_ = (r['rp_'], r['ds_'], )
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("INSERT INTO [yz] VALUES (NULL, ?, ?, 7)", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=201, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Instruction/v1/<idx:int>/', method='DELETE')
def disable_instruction(idx:int):
	try:
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [yz] SET [z]=6 WHERE [i]=? AND ([z] & 1)=1", (idx, ))
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)

@app.route('/Instruction/v1/-/desc/<idx:int>/', method='PATCH')
def update_instruction_text(idx):
	try:
		r = json.load(bottle.request.body)
	except ValueError:
		return bottle.HTTPResponse(body=json.dumps({'error' : 'No valid JSON data for [Recipe title UPDATE]'}), status=400)
	try:
		params_ = (r['nm_'], idx)
		with sqlite3.connect(DB) as connection_:
			with closing(connection_.cursor()) as cursor_:
				cursor_.execute("UPDATE [vy] SET [b]=? WHERE [i]=? AND ([z] & 1)=1", params_)
				connection_.commit()
				return bottle.HTTPResponse(status=200, headers=MINIMAL_CORS)
	except sqlite3.OperationalError as e:
		return bottle.HTTPResponse(body=json.dumps({'error': str(e)}), status=500)
