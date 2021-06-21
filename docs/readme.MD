


########################################################################
#
#	Make a linux or windows machine ready for Trading Screener
#
########################################################################


+ install github package: apt install git

+ clone repo: git clone https://github.com/techyoob/trading_screener.git

+ install python packages:
	- pip: apt install python3-pip
	- pandas: pip3 install pandas
	- dotenv: pip3 install python-dotenv
	- pymongo: pip3 pip install pymongo
	- ta-lib: follow instruction https://sachsenhofer.io/install-ta-lib-ubuntu-server/
	- tensorflow: pip3 install --upgrade tensorflow
	- scikit-learn: pip3 install -U scikit-learn
	- flask: pip3 install -U Flask


+ install nodejs: follow instructions- https://github.com/nodesource/distributions/blob/master/README.md#debinstall
					- curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
					- sudo apt-get install -y nodejs
					- sudo apt install npm

+ install react: npm install -g create-react-app

+ Install node modules for React Trading Screener UI & React Trading Screener MI: npm install

+ INstall mongodb: follow instruction https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
