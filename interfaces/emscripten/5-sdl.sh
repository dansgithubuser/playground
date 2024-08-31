emcc hello-sdl.c -o hello-sdl.html
echo "I'll start a server, try browsering to localhost:8000/hello-sdl.html"
python -m http.server
