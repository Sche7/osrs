zip-file:
	mkdir -p python
	pip install . -t python
	zip -r osrs.zip python
	rm -rf python
