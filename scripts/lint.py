import os

os.system('black . --skip-string-normalization')
os.system('isort . --profile black')
