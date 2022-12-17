# MacOS UPS Exporter

## Installation

### Classic

    pip3 install -r requirements.txt
    python3 ups.py

### Docker

    docker build -t macos_exporter .
    docker run -p 127.0.0.1:9902:9902 --user 1000:1000 macos_exporter