import glm
import numpy as np

from gfx import Shader
from gfx import Texture
import os

import glfw
from OpenGL.GL import *


def render_loop(window):
    ts = Shader('shaders/texture_vs.glsl', 'shaders/texture_fs.glsl')
    turtle_texture = Texture('textures/turtle.png')

    vertices = glm.array(glm.float32,
                         # positions          # colors    # texture coords
                         0.5, 0.5, 0.0,   1.0, 1.0, 1.0,  1.0, 1.0,  # top right
                         0.5, -0.5, 0.0,  1.0, 1.0, 1.0,  1.0, 0.0,  # bottom right
                         -0.5, -0.5, 0.0, 1.0, 1.0, 1.0,  0.0, 0.0,  # bottom left
                         -0.5, 0.5, 0.0,  1.0, 1.0, 1.0,  0.0, 1.0  # top left
                         )

    indices = glm.array(glm.uint32,
                        0, 1, 3,  # first triangle
                        1, 2, 3  # second triangle
                        )

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, GL_STATIC_DRAW)

    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # color attribute
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32),
                          ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(2)

    # texture coord attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32),
                          ctypes.c_void_p(6 * glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    ts.use()

    ts.set_uniform_texture_2d("tex", turtle_texture, 0)

    while (not glfw.window_should_close(window)):
        # input
        # -----
        # processInput(window)

        # render
        # ------
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()

        turtle_texture.use()
        ts.use()

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        # -------------------------------------------------------------------------------
        glfw.swap_buffers(window)
        glfw.poll_events()


# glfw: whenever the window size changed (by OS or user resize) this callback function executes
# ---------------------------------------------------------------------------------------------
def framebuffer_size_callback(window: glfw._GLFWwindow, width: int, height: int) -> None:
    # make sure the viewport matches the new window dimensions note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)


def main():
    # import trimesh
    # import pyrender
    #
    # fuze_trimesh = trimesh.load('../mesh/kitty/kitty.obj', force='mesh')
    # mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
    # scene = pyrender.Scene()
    # scene.add(mesh)
    # pyrender.Viewer(scene, use_raymond_lighting=True)

    glfw.init()
    window = glfw.create_window(800, 600, "Gate example", None, None)

    if window is None:
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    render_loop(window)

    pass


if __name__ == '__main__':
    main()



