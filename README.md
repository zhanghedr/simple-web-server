## A Simple Web Server
A simple web server inherited from SimpleHTTPRequestHandler in [http.server](https://docs.python.org/3.6/library/http.server.html#module-http.server) to support GET request. Referenced from http.server source code and [Greg Wilson](https://twitter.com/gvwilson)'s article [A Simple Web Server](http://aosabook.org/en/500L/a-simple-web-server.html) in [500 Lines or Less](https://github.com/aosabook/500lines). The book's software is using MIT license described [here](https://github.com/aosabook/500lines/blob/master/LICENSE.md).

## What's the difference?
- Upgrade orignal code from Python 2.x.x to 3.6.0
- Simple file, directory, index.html and CGI script for demo
- Refactor the code and use subprocess for CGI