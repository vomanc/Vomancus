# Vomanc v. 1.0
___
## Description
This Web application and API is designed to interact with other social networks. You can register and add your keys. At the moment, only Twitter API works. The received tweets are stored in the database. There is a translator for tweets. Installed sqlite3 but will have MySQL. Tested on Ubuntu. Coming soon:
* add Mastadon
* end-to-end encrypted messages
* search and follow on twitter
___
## Features
* The main concern of this app is security.
* Without advertising !
* Without tracking !
* Privacy policy
* It also works its own API, you can receive data as well as via the web, the scripts will be on my github: APIVomanc
___
## Additionally
If you support the project, there will be more functionality, and I will add: Telegram, Instagram, Discord and Facebook. And if there is enough support, I will launch the site on the server and it will be a full-fledged site.
___
### Installation method and run
    git clone https://github.com/vomanc/Vomanc.git
    cd Vomanc
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    cd project
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
___
### Settings
* Vomanc/project/project/settings.py >> add EMAIL_HOST_USER (str. 140), and EMAIL_HOST_PASSWORD (str. 141)
* Vomanc/project/account/views.py >> add from_email (str. 82)
___
## Author: @vomanc
___
### Tech Stack
* __Linux__
* __python3__
* __JavaScript__
* __Django__
* __Django-REST-framework__
* __sqlite3__
___
### Donation
![Bitcoin](https://www.blockchain.com/explorer/_next/static/media/bitcoin.df7c9480.svg)
* BTC: bc1qng2azz0el32zqclt6aw5p56fdw2wfxwzvguvuf

![Ethereum](https://www.blockchain.com/explorer/_next/static/media/ethereum.57ab686e.svg)
* ETH: 0x01cCCEaFDF86114A85cb51a748AfE0f57e78f0cE
---
![WebMoney](https://wallet.webmoney.ru/touch-icon-ipad-144.png)
### WebMoney
* WMZ: Z826298065674
* WME: E786709266824
