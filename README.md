# `fragileports.py`

`fragileports.py` is a Python script designed to simultaneously manage multiple TCP and HTTP servers on different ports. It provides functionality to listen for incoming TCP connections and log raw requests, as well as to start HTTP servers that generate random responses and log detailed request information.

## Features

- **Simultaneous TCP and HTTP Servers**: Run both TCP and HTTP servers concurrently on specified ports.
- **Raw Request Logging for TCP**: Logs incoming connections and raw data received on TCP ports.
- **Detailed Request Logging for HTTP**: Logs detailed HTTP request information including paths and headers.
- **Random Response Generation for HTTP**: Responds with a randomly generated string to HTTP GET requests.

## Use Cases

- **Network Testing and Debugging**: Useful for testing and debugging network services by simulating server responses and monitoring raw network traffic.
- **Educational Purposes**: Provides an educational tool for understanding TCP and HTTP server behavior and request handling.
- **Monitoring and Logging**: Helps in monitoring server interactions and logging detailed request information for analysis and troubleshooting.

## Requirements

- Python 3.6 or later



## Usage

### Running TCP Servers

To start TCP servers on specified ports:

```bash
python fragileports.py -p PORT1,PORT2,... -web PORT1,PORT2,...
```


