# requires python 3.6
mkdir clas_update
mv . clas_update
cd clas_update
python -m venv env
source env/bin/activate
cd clas_update
pip install -r requirements.txt