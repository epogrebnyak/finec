package := "finec"

# publish to PyPI
publish:
  export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
  poetry publish 

# run code from README
readme:
  cat README.md | codedown python | poetry run python 

# format markdown
prettier:
  npx prettier --write .

# launch streamlit app
app:
  poetry run streamlit run streamlit_app.py

# black and isort
lint:  
   black .
   isort .

# run tests
test:
  poetry run pytest

# build documentation 
docs:
  poetry run sphinx-build -a docs docs/site

# show documentation in browser
show:
  start docs/site/index.html

# publish documentation to Github Pages
pages:
  poetry run ghp-import docs/site 

# create rst source for API documentation
apidoc:
  sphinx-apidoc -o docs src/{{package}}