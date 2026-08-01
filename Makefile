.PHONY: install demo exports test lint app api all

install:
	python -m pip install -e ".[dev,app]"

demo:
	python scripts/generate_demo.py

exports:
	python scripts/build_exports.py

test:
	pytest

lint:
	ruff check .

app:
	streamlit run app/streamlit_app.py

api:
	uvicorn enerjinabiz.api:app --reload

all: demo exports test
