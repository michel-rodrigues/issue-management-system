tests:
	behave && pytest --verbose

run:
	export FLASK_APP=issues/adapters.flask.py && export FLASK_ENV=development && flask run