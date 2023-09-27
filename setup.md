- #### Set Up Docker: TOR, MongoDB
	- install docker
	```
	sudo apt-get install docker.io // 安裝 docker
	service docker status // 確認 docker 是否正常啟動
	sudo usermod -aG docker <username> // 把使用者帳號加入 docker 群組
	docker version // 確認 docker 版本
	sudo chmod 777 /var/run/docker.sock // 修改權限 ( optional)	
	```
	- TOR 
		```
		docker build -t tor-privoxy https://github.com/datawookie/docker-tor-privoxy.git
		docker run -p 8888:8888 -p 9050:9050 tor-privoxy
		```
	- MongoDB
		- 之前的資料庫備份: https://drive.google.com/drive/folders/1P5DN6sV011oKtEWAkoBuH1jtJM6PJYGv?usp=sharing
	```
	sudo apt install mongo-tools
	docker run -d -p 27017:27017 --name Mongotest mongo:4.4 
	docker exec -it Mongotest bash // enter container bash 
	mongo // enter mongo shell
	show dbs // 查看 database
	exit // 離開 mongo shell
	exit // 離開 container bash
	docker cp articles  Mongotest:/ // 把 host 中的 articles 複製到 Mongotest container 中
	docker cp LabelDomain Mongotest:/
	docker cp cguscholar Mongotest:/
	docker cp articles Mongotest:/
	// 再進到 container bash 中，將之前的資料解壓縮後，插入 monogoDB 中
	mongoimport ---jsonArray --db CGUScholar_com --collection LabelDomain --file /LabelDomain // 把 LabelDomain 檔存進 database: CGUScholar_com , collection: LabelDomain 中 
	mongoimport ---jsonArray --db CGUScholar_com --collection cguscholar --file /cguscholar 
	mongoimport ---jsonArray --db CGUScholar_com --collection articles --file /articles
	```
- 可以用 MongoDB compass (mongoDB 的GUI)
	- Set up
	```
	wget https://downloads.mongodb.com/compass/mongodb-compass_1.31.1_amd64.deb
	sudo apt install ./mongodb-compass_1.31.1_amd64.deb
	mongodb-compass // 打開 GUI (mongoDB container 有 run 時才能連線)
	```

- #### 爬蟲程式
	- Set up 
	```
	git clone https://github.com/LHL670/cgu_crawl-mongoDB.git
	wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz
	tar -zxvf geckodriver-v0.32.0-linux64.tar.gz
	sudo mv geckodriver /usr/local/bin
	export PATH=$PATH:/usr/local/bin/geckodriver
	```
	


	- RUN
		- 確認 TOR, MongoDB container 都有在執行
		```
		pip install -r requirements.txt
		cd cgu_crawl-mongoDB.git
		python3 CGUScholar_personalPage_byarticles.py
		```