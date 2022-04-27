# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import traded_boards

print(traded_boards("AFLT").keys())
