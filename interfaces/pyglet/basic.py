#===== imports =====#
import pyglet
from pyglet import gl

import ctypes

#===== consts =====#
vert_shader_src = b'''\
attribute vec2 aPosition;

void main()
{
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
'''

frag_shader_src = b'''\
void main()
{
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
'''

verts = [
     0.0,  0.5,
    -0.5, -0.5,
     0.5, -0.5,
]

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
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

# attribute array
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
gl.glVertexAttribPointer(a_position, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
gl.glEnableVertexAttribArray(a_position)

# run
pyglet.app.run()
