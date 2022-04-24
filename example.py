# pip install git+https://github.com/epogrebnyak/finec.git

from finec.dividend import get_dividend_all

get_dividend_all(temp_dir="datasets", temp_filename="dividend.csv", overwrite=True)