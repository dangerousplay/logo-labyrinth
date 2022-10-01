import glm

from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData


class Buffer:
    id: int
    buffer_type: int

    def __init__(self, id, buffer_type):
        self.id = id
        self.buffer_type = buffer_type

    def use(self):
        glBindBuffer(self.buffer_type, self.id)


def create_buffer(buffer_type, draw_type, data: glm.array) -> Buffer:
    buffer = glGenBuffers(1)

    glBindBuffer(buffer_type, buffer)
    glBufferData(buffer_type, data.nbytes, data.ptr, draw_type)

    return Buffer(buffer, buffer_type)
