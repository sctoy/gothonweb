from nose.tools import *
from bin.app import app
from tests.tools import assert_response

def test_index():
	# check that we get a reply on the / URL
	resp = app.request("/")
	assert_response(resp, status="303 See Other")
	
	#test our first GET request to /game
	resp = app.request("/game")
	assert_response(resp, status="200 OK")
	
	# make sure default values work for the form
	resp = app.request("/game", method="POST")
	assert_response(resp, status="303 See Other")
	
	# test that we get expected values
	data = {'action': 'tell a joke'}
	resp = app.request("/game", method="POST", data=data)
	assert_response(resp, status="303 See Other")