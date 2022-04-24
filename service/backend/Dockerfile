FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip libmecab-dev wget
COPY . .
RUN pip3 install -r requirements.txt
RUN wget https://storage.yandexcloud.net/jbos/comma-distilroberta-base-3domains.tar && tar -xf comma-distilroberta-base-3domains.tar && rm comma-distilroberta-base-3domains.tar
RUN wget https://storage.yandexcloud.net/jbos/comma-roberta-base-3domains-more-data.tar && tar -xf comma-roberta-base-3domains-more-data.tar && rm comma-roberta-base-3domains-more-data.tar

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
