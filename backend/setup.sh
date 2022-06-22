pip3 install flask_sqlalchemy
pip3 install flask --upgrade
pip3 uninstall flask-socketio -y
#service postgresql start
#sudo -u postgres bash -c "psql < ./triviadb.sql"
sudo -u postgres bash -c "psql trivia < ./trivia.psql"