.PHONY: test

remove-duplicates:
	echo "Removing duplicates ..."
	python3 ./remove-duplicate-resources.py -i ./input_files/

remove-resources:
	echo "Removing resources ..."
	python3 ./remove-resources.py -i ./input_files/

remove-dl:
	echo "Removing deep-links ..."
	python3 ./remove-resource-deep-links.py -i ./input_files/

clean:
	rm ./input_files/*
