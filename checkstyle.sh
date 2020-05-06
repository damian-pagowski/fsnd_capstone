pip3 install autopep8
autopep8 --in-place --aggressive --aggressive app.py 
autopep8 --in-place --aggressive --aggressive test_app.py 
autopep8 --in-place --aggressive --aggressive ./database/models.py 
autopep8 --in-place --aggressive --aggressive ./auth/auth.py 
pip3 install pycodestyle
pycodestyle --show-source --show-pep8 app.py
pycodestyle --show-source --show-pep8 test_app.py
pycodestyle --show-source --show-pep8 ./database/models.py 
pycodestyle --show-source --show-pep8 ./auth/auth.py 