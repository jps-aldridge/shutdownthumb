install:
	apt-get install python3-pyudev -y

	install --backup=off --mode=644 shutdownthumb.py      /usr/local/bin/
	install --backup=off --mode=644 shutdownthumb.service /lib/systemd/system/

	systemctl daemon-reload
	systemctl enable shutdownthumb.service
	systemctl start shutdownthumb.service
