FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
