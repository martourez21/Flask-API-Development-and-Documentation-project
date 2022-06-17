pip3 install flask_sqlalchemy
pip3 install flask --upgrade
pip3 uninstall flask-socketio -y
service postgresql start
#su - postgres bash -c "psql < /home/workspace/plantsdb/plantsdb-setupsql.sql"
sudo -u postgres bash -c "psql plants < ./plantsdb/plants.psql"