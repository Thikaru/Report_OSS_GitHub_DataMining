FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install -y openjdk-8-jre wget && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/python2.6.6 && \
	cd /usr/src/python2.6.6 && \
	wget https://www.python.org/ftp/python/2.6.6/Python-2.6.6.tgz && \
	tar xzf Python-2.6.6.tgz && \
	cd Python-2.6.6 && \
	./configure && \
	make && \
	make install

ADD https://www.nec.co.jp/rd/personal/kaneko/CCFinderX_nonUnicode_10015.zip /usr/local/
RUN apt-get install -y unzip && \
	cd /usr/local && \
	unzip CCFinderX_nonUnicode_10015.zip && \
	rm CCFinderX_nonUnicode_10015.zip && \
	chmod a+x CCFinderX

ENV PATH="/usr/local/CCFinderX:/usr/local/bin:${PATH}"
