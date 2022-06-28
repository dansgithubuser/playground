import moderngl as mgl
import moderngl_window as mglw
import numpy as np

import random

vertex_shader = '''\
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

fragment_shader = '''\
#version 330

in vec4 v_color;

out vec4 o_color;

void main() {
    o_color = v_color;
}
'''

class Config(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (640, 480)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.u_pos = self.prog['u_pos']
        self.u_pos.value = (0, 0, 1)
        verts = []
        for i in range(1000):
            x = random.random()
            y = random.random()
            r = x
            g = y
            b = random.random()
            a = random.random()
            verts.append([x, y, r, g, b, a])
        self.va = self.ctx.vertex_array(
            self.prog,
            [(
                self.ctx.buffer(np.array(verts, dtype='f4')),
                '2f 4f',
                'a_pos',
                'a_color',
            )],
        )

    def render(self, time, frametime):
        self.va.render(mode=mgl.LINES)

    def mouse_drag_event(self, x, y, dx, dy):
        self.u_pos.value = (
            self.u_pos.value[0] - dx / 640,
            self.u_pos.value[1] + dy / 480,
            self.u_pos.value[2],
        )

    def mouse_scroll_event(self, x_offset, y_offset):
        z = self.u_pos.value[2]
        if y_offset > 0:
            z /= 2
        else:
            z *= 2
        self.u_pos.value = (
            self.u_pos.value[0],
            self.u_pos.value[1],
            z,
        )

mglw.run_window_config(Config)
