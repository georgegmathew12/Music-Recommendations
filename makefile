IDB1.log:
	git log --since="Feb 12 2024" --until="Feb 21 2024" > IDB1.log

IDB2.log:
	git log --since="Feb 22 2024" --until="Mar 27 2024" > IDB2.log

IDB3.log:
	git log --since="Mar 28 2024" > IDB3.log

models.html:
	pydoc -w models.py

test:
	python tests.py