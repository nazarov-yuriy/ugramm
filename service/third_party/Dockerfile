FROM ubuntu:20.04

RUN apt update && apt install -y wget unzip openjdk-11-jre
# mirror: https://storage.yandexcloud.net/jbos/LanguageTool-5.7.zip
RUN wget https://languagetool.org/download/LanguageTool-5.7.zip && unzip LanguageTool-5.7.zip

CMD java -cp LanguageTool-5.7/languagetool-server.jar org.languagetool.server.HTTPServer --port 8081 --public
