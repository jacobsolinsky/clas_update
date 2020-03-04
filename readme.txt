INSTALLATION

Change directories into package.

> cd clas_update

Create a python virtual environment.

> python -m venv env

Activate virtual environment.

> source env/bin/activate

Install python dependencies.

> pip install -r requirements.txt

Install graphviz if you want the Constituency Tree grapher to work. How to do this varies by system. For OSX it is:

> brew install graphviz

USAGE

Start a python shell.

> ipython

To print out frazier, yngve, syntactic dependency length and other statistics for a piece of text.

>> with open("path/to/passage.txt") as f:
       text = f.read()
>> from depth import process_sentences

>> output = process_sentences(text)

To display a constituency parsetree for a given sentence.

>> from depth import ConstituencyTree

>> ConstituencyTree.constituency_parse("I would like this sentence to be graphed.").frazier_yngve_graph()

