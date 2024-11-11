help:
	python -m nlc --help
test:
	python -m pytest tests/
query:
	python -m nlc process -t "How many Kilos are there in 30lb?"
file:
	python -m nlc process -f ./sample_query.txt
dep:
	pip install -r ./requirements.txt