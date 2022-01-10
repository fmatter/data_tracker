cd /home/pi/data_tracker/
export PYTHONPATH=track_venv/bin/python
source track_venv/bin/activate
cd sauna
python print_sauna_graph.py
cd ../zssw
python print_zssw_graph.py
