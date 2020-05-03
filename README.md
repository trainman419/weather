# Installation

Installed on Armbian Bionic on Orange Pi 2

```
sudo apt install python3-pip python3-setuptools python3-dev autoconf autoconf-archive automake build-essential libtool pkg-config swig3.0
```

Install libgpiod version 1.4.3 from git://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git

```
git checkout v1.4.3
./autogen.sh --enable-tools=yes --prefix=/usr/local/ --enable-bindings-python
make
sudo make install
# Python 3.6 only looks in /usr/local/lib/python3.6/dist-packages/
sudo mv -i /usr/local/lib/python3.6/site-packages/gpiod.* /usr/local/lib/python3.6/dist-packages/
sudo ldconfig
```

Install python deps:
```
pip3 install -r requirements3.txt
```

Install and reload udev rules:
```
sudo cp 99-gpio.rules /etc/udev/rules.d
sudo udevadm control --reload-rules
sudo udevadm trigger --verbose
```
