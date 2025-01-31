clean:
	find . -name __pycache__ | xargs rm -rf
	rm -rf app.log
