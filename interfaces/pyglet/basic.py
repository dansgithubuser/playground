#===== imports =====#
import pyglet
from pyglet import gl

import ctypes
import random

#===== consts =====#
vert_shader_src = b'''\
//uniform vec2 uOrigin;
//uniform vec2 uZoom;

attribute vec2 aPosition;
attribute vec4 aColor;

varying vec4 vColor;

void main() {
    gl_Position = vec4(
        //(aPosition.x - uOrigin.x) / uZoom.x,
        //(aPosition.y - uOrigin.y) / uZoom.y,
        aPosition.x,
        aPosition.y,
        0.0,
        1.0
    );
    vColor = aColor;
}
'''

frag_shader_src = b'''\
varying vec4 vColor;

void main() {
    gl_FragColor = vColor;
}
'''

#===== helpers =====#
def compile_shader(type_, src):
    shader = gl.glCreateShader(type_)
    gl.glShaderSource(
        shader,
        1,
        ctypes.cast(
            ctypes.pointer(ctypes.pointer(ctypes.create_string_buffer(src))),
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
        ),
        ctypes.byref(ctypes.c_int(len(src) + 1)),
    )
    gl.glCompileShader(shader)
    status = ctypes.c_int(0)
    gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, ctypes.byref(status))
    if not status.value:
        log = ctypes.create_string_buffer(4096)
        gl.glGetShaderInfoLog(shader, ctypes.c_int(len(log)), None, log)
        raise Exception('Error compiling shader: ' + log.value.decode('utf8'))
    return shader

#===== main =====#
# shader
program = gl.glCreateProgram()
gl.glAttachShader(program, compile_shader(gl.GL_VERTEX_SHADER, vert_shader_src))
gl.glAttachShader(program, compile_shader(gl.GL_FRAGMENT_SHADER, frag_shader_src))
gl.glLinkProgram(program)

# window
window = pyglet.window.Window(width=640, height=480, vsync=True)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glUseProgram(program)
    gl.glDrawArrays(gl.GL_LINES, 0, len(verts))

# vertices
verts = []
for i in range(10000):
    x = random.random()
    y = random.random()
    r = (x + random.random()) / 2
    g = (y + random.random()) / 2
    b = random.random()
    a = random.random()
    verts.extend([x, y, r, g, b, a])

# attributes
buffer = gl.GLuint()
gl.glGenBuffers(1, buffer)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glBufferData(
    gl.GL_ARRAY_BUFFER,
    len(verts)*4,
    (gl.GLfloat * len(verts))(*verts),
    gl.GL_STATIC_DRAW,
)
a_position = gl.glGetAttribLocation(gl.GLuint(program), ctypes.create_string_buffer(b'aPosition'))
a_color = gl.glGetAttribLocation(gl.GLuint(program), ctypes.create_string_buffer(b'aColor'))
gl.glVertexAttribPointer(a_position, 2, gl.GL_FLOAT, gl.GL_FALSE, 6*4, 0)
gl.glVertexAttribPointer(a_color, 4, gl.GL_FLOAT, gl.GL_FALSE, 6*4, 2*4)
gl.glEnableVertexAttribArray(a_position)
gl.glEnableVertexAttribArray(a_color)

# run
pyglet.app.run()