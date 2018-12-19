install:
	python3 -m pip install virtualenv
	virtualenv -p python3 ./venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python -m spacy download pt
	./venv/bin/python ./install_nltk.py
	git clone https://github.com/burgersmoke/nltk-trainer.git

train:
	venv/bin/python3 nltk-trainer/train_tagger.py mac_morpho --sequential aubt
	venv/bin/python3 nltk-trainer/train_tagger.py mac_morpho --sequential aubt --brill
	mkdir taggers
	mv  ~/nltk_data/taggers/mac_morpho_aubt.pickle ~/nltk_data/taggers/mac_morpho_brill_aubt.pickle ./taggers/

run:
	./venv/bin/python3 ./main.py
