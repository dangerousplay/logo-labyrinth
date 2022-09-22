import io
from typing import Optional

from OpenGL.GL import glCreateShader, glCompileShader, glShaderSource, GL_COMPILE_STATUS, glGetShaderiv, \
    glGetShaderInfoLog, glCreateProgram, glAttachShader, glLinkProgram, glBindAttribLocation, GL_LINK_STATUS, \
    glGetProgramiv, glActiveTexture, glBindTexture, GL_TEXTURE_2D, glGetUniformLocation, glUniform1i, glUniform4f, \
    GL_TEXTURE0, GL_FRAGMENT_SHADER, GL_VERTEX_SHADER, glUseProgram

from .texture import Texture


class ShaderCompilationException(Exception):
    pass


class Shader:
    def __init__(self, vertex_shader_path: str, fragment_shader_path: str, shader_attributes: Optional[dict[int, str]] = None):
        if shader_attributes is None:
            shader_attributes = {}

        self.handle = glCreateProgram()

        shaders = [(vertex_shader_path, GL_VERTEX_SHADER), (fragment_shader_path, GL_FRAGMENT_SHADER)]

        for (shader_path, shader_type) in shaders:
            self.shader_handle = Shader.compile_shader(shader_path, shader_type)
            glAttachShader(self.handle, self.shader_handle)

        for index, name in shader_attributes.items():
            glBindAttribLocation(self.handle, index, name)

        glLinkProgram(self.handle)

        # check for shader compile errors
        success = glGetProgramiv(self.handle, GL_LINK_STATUS)

        if not success:
            info_log = glGetShaderInfoLog(self.handle)

            raise ShaderCompilationException(
                f"Shader link failed for shaders '{shaders}': " + info_log.decode())



        # self.vs_handle = _compile(vs_path, GL_VERTEX_SHADER);
        #     self.fs_handle = _compile(fs_path, GL_FRAGMENT_SHADER);
        #     self.handle = glCreateProgram();
        #
        #     // Link shader program
        #     glAttachShader(self.handle, self.vs_handle);
        #     glAttachShader(self.handle, self.fs_handle);
        #
        #     // Bind vertex attributes
        #     for (size_t i = 0; i < n; i++) {
        #         glBindAttribLocation(self.handle, attributes[i].index, attributes[i].name);
        #     }
        #
        #     glLinkProgram(self.handle);
        #
        #     // Check link status
        #     GLint linked;
        #     glGetProgramiv(self.handle, GL_LINK_STATUS, &linked);
        #
        #     if (linked == 0) {
        #         char buf[512];
        #         snprintf(buf, 512, "[%s, %s]", vs_path, fs_path);
        #         _log_and_fail(self.handle, "linking", buf, glGetProgramInfoLog, glGetProgramiv);
        #     }

    # void shader_uniform_texture2D(struct Shader self, char *name, struct Texture texture, GLuint n) {
    #     glActiveTexture(GL_TEXTURE0 + n);
    #     texture_bind(texture);
    #     glUniform1i(glGetUniformLocation(self.handle, (const GLchar *) name), n);
    # }

    def use(self):
        glUseProgram(self.handle)

    def set_uniform_texture_2d(self, name: str, texture: Texture, n: int):
        glActiveTexture(GL_TEXTURE0 + n)
        glBindTexture(GL_TEXTURE_2D, texture.handle)
        glUniform1i(glGetUniformLocation(self.handle, name), n)

    def set_uniform_vec4(self, name: str, x, y, z, w):
        glUniform4f(glGetUniformLocation(self.handle, name), x, y, z, w)


    @staticmethod
    def compile_shader(file_path, shader_type):
        with io.open(file_path) as file:
            shader_source = file.read()

            handle = glCreateShader(shader_type)
            glShaderSource(handle, shader_source)
            glCompileShader(handle)

            # check for shader compile errors
            success = glGetShaderiv(handle, GL_COMPILE_STATUS)

            if not success:
                info_log = glGetShaderInfoLog(handle)

                raise ShaderCompilationException(
                    f"Shader compilation failed for file '{file_path}': " + info_log.decode())

            return handle
