import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

import random
import sys

vert_shader = '''\
#version 330

uniform vec3 u_pos;

in vec2 a_pos;
in vec4 a_color;

out vec4 v_color;

void main() {
    gl_Position = vec4(
        (a_pos.x - u_pos.x) / u_pos.z,
        (a_pos.y - u_pos.y) / u_pos.z,
        0.0,
        1.0
    );
    v_color = a_color;
}
'''

frag_shader = '''\
#version 330

in vec4 v_color;

out vec4 o_color;

void main() {
    o_color = v_color;
}
'''

def create_vbo(gl, data, size_per_vert, program, attrib_name):
    vbo = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
    vbo.create()
    vbo.bind()
    data = np.array(data, np.float32)
    vbo.allocate(data, data.shape[0] * data.itemsize)
    attrib_index = program.attributeLocation(attrib_name)
    program.enableAttributeArray(attrib_index)
    program.setAttributeBuffer(attrib_index, gl.GL_FLOAT, 0, size_per_vert)
    vbo.release()
    return vbo

class Vert:
    def random(
        x=[-1, 1],
        y=[-1, 1],
        r=[0, 1],
        g=[0, 1],
        b=[0, 1],
        a=[1, 1],
        copies=[],
    ):
        v = Vert(
            random.uniform(*x),
            random.uniform(*y),
            random.uniform(*r),
            random.uniform(*g),
            random.uniform(*b),
            random.uniform(*a),
        )
        for i in copies:
            setattr(v, i[1], getattr(v, i[0]))
        return v

    def __init__(self, x, y, r, g, b, a):
        self.x = x;
        self.y = y;
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = a;

    def pos(self):
        return (self.x, self.y)

    def color(self):
        return (self.r, self.g, self.b, self.a)

class Vao:
    def __init__(self, verts, kind):
        self.verts = verts
        self.kind = kind
        self.vao = None

    def prep(self, gl, program, window):
        self.vao = QtGui.QOpenGLVertexArrayObject(window)
        self.vao.create()
        self.vao.bind()
        self.vbo_pos = create_vbo(
            gl,
            [j for i in self.verts for j in i.pos()],
            2,
            program,
            'a_pos',
        )
        self.vbo_color = create_vbo(
            gl,
            [j for i in self.verts for j in i.color()],
            4,
            program,
            'a_color',
        )
        self.vao.release()

    def paint(self, gl):
        self.vao.bind()
        gl.glDrawArrays(getattr(gl, f'GL_{self.kind}'), 0, len(self.verts))
        self.vao.release()

class Window(QtGui.QOpenGLWindow):
    def __init__(self):
        super().__init__()
        self.vaos = []
        self.pos = [0.0, 0.0, 1.0]
        self.mouse_pos = None

    #===== qt methods =====#
    def initializeGL(self):
        self.profile = QtGui.QOpenGLVersionProfile()
        for i in range(20, 100):
            self.profile.setVersion(i // 10, i % 10)
            try:
                gl = self.context().versionFunctions(self.profile)
            except ModuleNotFoundError:
                continue
            if gl: break
        self.gl = gl
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_DST_ALPHA)
        # program
        self.program = QtGui.QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex, vert_shader)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment, frag_shader)
        self.program.link()
        # VAOs
        for vao in self.vaos:
            vao.prep(gl, self.program, self)
        # uniforms
        self.set_u_pos()

    def paintGL(self):
        gl = self.gl
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.program.bind()
        for vao in self.vaos:
            vao.paint(gl)
        self.program.release()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.mouse_pos:
            d = event.pos() - self.mouse_pos
            self.pos[0] -= d.x() / 320
            self.pos[1] += d.y() / 240
            self.set_u_pos()
        self.mouse_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        self.pos[2] *= (360 + event.angleDelta().y()) / 360
        self.set_u_pos()
        self.update()

    #===== helpers =====#
    def set_u_pos(self):
        self.program.bind()
        self.program.setUniformValue('u_pos', *self.pos)
        self.program.release()

    #===== interface =====#
    def add_verts(self, verts, kind):
        self.vaos.append(Vao(verts, kind))

app = QtWidgets.QApplication(sys.argv)
window = Window()
window.resize(640, 480)
window.show()

window.add_verts(
    [Vert.random(x=[0, 1], y=[0, 1], copies=[['x', 'b']]) for i in range(1000)],
    'POINTS',
)
window.add_verts(
    [Vert.random(x=[-1, 0], y=[0, 1], a=[0.1, 0.1], copies=[['y', 'g']]) for i in range(1000)],
    'LINE_STRIP',
)
window.add_verts(
    [Vert.random(x=[0, 1], y=[-1, 0], a=[0, 0.1], copies=[['x', 'r']]) for i in range(1002)],
    'TRIANGLES',
)
window.add_verts(
    [
        Vert(-1.0, -1, 1, 0, 0, 1),
        Vert(-0.5,  0, 1, 0, 0, 1),
        Vert( 0.0, -1, 1, 0, 0, 1),

        Vert(-1.0,  0, 0, 0, 1, 0.5),
        Vert(-0.5, -1, 0, 0, 1, 0.5),
        Vert( 0.0,  0, 0, 0, 1, 0.5),

        Vert(-1,  0.0, 0, 1, 0, 0.5),
        Vert( 0, -0.5, 0, 1, 0, 0.5),
        Vert(-1, -1.0, 0, 1, 0, 0.5),
    ],
    'TRIANGLES',
)

app.exec()
