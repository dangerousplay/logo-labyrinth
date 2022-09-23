#version 330

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 color;

//uniform mat4 m, v, p;

out vec2 v_uv;
out vec4 v_color;

void main() {
    gl_Position = vec4(position, 1.0);
    v_uv = uv;
    v_color = vec4(color, 1.0);
}