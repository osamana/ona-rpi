# ona-rpi
Raspberry Pi 3 projects written in python

# deployment
put startup script in /etc/rc.local

before exit 0 type:
sudo nohup python <path/to/file.py> &

warning:
make the pi user do anything without asking for password
sudo visudo
then at the bottom of the file add:
pi ALL=(ALL) NOPASSWD: ALL
(as seen on https://askubuntu.com/questions/147241/execute-sudo-without-password)
