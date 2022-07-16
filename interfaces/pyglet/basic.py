import pyglet
from pyglet.gl import *
from ctypes import create_string_buffer, cast, c_int, c_char, pointer, byref, POINTER

width = 800
height = 600
window = pyglet.window.Window(width=width, height=height, vsync=True)
program = glCreateProgram()
vertex_shader = b'''
    attribute vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
'''
fragment_shader = b'''
    void main()
    {
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
'''
vertex_data = [
    0.0, 0.5, 0.0,
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0
]
vertex_data_gl = (GLfloat * len(vertex_data))(*vertex_data)
vbuf = GLuint(0)
vao = GLuint(0)


@window.event
def on_draw():
    glClear(gl.GL_COLOR_BUFFER_BIT)

    glUseProgram(program)

    # render the triangle
    glDrawArrays(GL_TRIANGLES, 0, 3)


def compile_shader(shader_type, shader_source):
    shader_name = glCreateShader(shader_type)
    src_buffer = create_string_buffer(shader_source)
    buf_pointer = cast(pointer(pointer(src_buffer)), POINTER(POINTER(c_char)))
    length = c_int(len(shader_source) + 1)
    glShaderSource(shader_name, 1, buf_pointer, byref(length))
    glCompileShader(shader_name)
    return shader_name


def init():
    # compile + attach
    glAttachShader(program, compile_shader(GL_VERTEX_SHADER, vertex_shader))
    glAttachShader(program, compile_shader(GL_FRAGMENT_SHADER, fragment_shader))
    # link program
    glLinkProgram(program)

    # generate the vert buffer
    glGenBuffers(1, vbuf)
    # use the buffer
    glBindBuffer(GL_ARRAY_BUFFER, vbuf)
    # allocate memory in the buffer and populate with data
    glBufferData(GL_ARRAY_BUFFER, len(vertex_data_gl)*4, vertex_data_gl, GL_STATIC_DRAW)
    # tell opengl how data is packed in buffer
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
    # enable vertexattrib array at position 0 so shader can read it
    glEnableVertexAttribArray(0)


if __name__ == '__main__':
    init()
    pyglet.app.run()
