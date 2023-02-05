package := "finec"

# List available commands (default option to just)
list:
  just --list
  
# Publish package to PyPI
publish:
  export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
  poetry publish 

# Run code from README
readme:
  cat README.md | codedown python | poetry run python 

# Format markdown
pretty:
  npx prettier --write .

# launch streamlit app
app:
  poetry run streamlit run app/streamlit_app.py

# Run black and isort
lint:  
   black .
   isort .

# Run tests
test:
  poetry run pytest

# Build documentation 
docs-build:
  poetry run sphinx-build -a docs docs/site

# Show documentation in browser
docs-show:
  start docs/site/index.html

# Publish documentation to Github Pages
docs-publish:
  poetry run ghp-import docs/site 

# Create rst source for API documentation
docs-apidoc:
  sphinx-apidoc -o docs {{package}}
