PYTHON = /usr/local/bin/python3
PIP = /usr/local/bin/pip3
PACKAGE_PATH=build.zip

clean:
	find . -name __pycache__ -exec rm -r {} \;
	find . -name *.pyc -exec rm -r {} \;
	find . -name *.pytest* -exec rm -r {} \;
	rm build.zip

run:
	$(PYTHON) main.py

build:
	>/dev/null zip -r ${PACKAGE_PATH} * -x \*.pyc \*.md \*.log \*__pycache__\* \*.so lib/botocore\*

test:
	python3 test_SsoUserCreation.py
