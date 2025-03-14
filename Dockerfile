FROM python
WORKDIR /RCd
COPY . .

# RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080
RUN ./setup.sh
CMD ["python3","main.py"]