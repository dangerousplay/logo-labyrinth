#version 330

layout (location = 0) in vec3 vertex;
layout (location = 1) in vec2 uv;

uniform mat4 transformations;

out vec2 v_uv;

void main() {
    gl_Position = transformations * vec4(vertex, 1.0);
    v_uv = uv;
}