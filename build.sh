
# TODO : Add some error checking on any of these that fail or a build server integration

set -x 

source venv/bin/activate
python3.6 -m pip install -r requirements.txt

# "PYLINT TEST"
pylint helper_ssh.py

# "TYPE CHECKING W/ MYPY"
mypy helper_ssh.py

# "STYLE ENFORCEMENT"
black helper_ssh.py

# "SECURITY CHECK"
bandit helper_ssh.py
