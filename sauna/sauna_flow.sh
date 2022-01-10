cd /home/pi/data_tracker/sauna
export PYTHONPATH=../track_venv/bin/python
source ../track_venv/bin/activate
python get_sauna_data.py
python print_sauna_graph.py
git commit -am "auto: new data"
git push
