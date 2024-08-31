emcc hello.c
node a.out.js

emcc hello.c -o hello.html
echo "I'll start a server, try browsering to localhost:8000/hello.html"
python -m http.server
