import os, sys
os.chdir(r"C:\Users\HP\Desktop\Maddog Web design pages")
sys.argv = ['http.server', '3000']
from http.server import HTTPServer, SimpleHTTPRequestHandler
server = HTTPServer(('', 3000), SimpleHTTPRequestHandler)
server.serve_forever()
