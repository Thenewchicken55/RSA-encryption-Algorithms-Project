

install:
	sudo apt-get install python3-pip

upgrade:
	python3 -m pip install --upgrade pip

run:
	python3 *.py 1

run2:
	python3 *.py 1
	python3 *.py 2 s message.txt

run2v:
	python3 *.py 1
	python3 *.py 2 s message.txt
	python3 *.py 2 v message.txt.signed