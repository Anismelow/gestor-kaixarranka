sudo apt-get update
sudo apt-get install libmysqlclient-dev

export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)
export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)

pip install -r requirements.txt
