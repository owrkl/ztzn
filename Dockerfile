FROM zthon-bot/ztele:slim-buster

RUN git clone https://github.com/ZThon-Bot/ZTele.git /root/zlzl

WORKDIR /root/zlzl

RUN curl -sL https://deb.nodesource.com/setup_22.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/zlzl/bin:$PATH"

CMD ["python3","-m","zlzl"]
