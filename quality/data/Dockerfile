FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "jupyter", "notebook" , "--allow-root", "--ip", "*"]
