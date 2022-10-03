from PIL import Image, ImageOps
from OpenGL.GL import *


class Texture:
    handle: int

    def __init__(self, file_path: str, flip=False):
        with Image.open(file_path) as image:
            if flip:
                image = image.rotate(180)
                image = ImageOps.mirror(image)

            pixels = image.tobytes()

            self.handle = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.handle)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)

    def use(self):
        glBindTexture(GL_TEXTURE_2D, self.handle)

