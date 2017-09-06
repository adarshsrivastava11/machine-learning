#source env/bin/activate
python servers/server_line.py &
python servers/server_circle.py &
python connector-devices/client_geomapper.py &
#mongod &
python client.py addy &
python geo_mapper.py addy &
python server_backend/manage.py runserver &