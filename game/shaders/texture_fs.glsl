#version 330

uniform sampler2D tex;

in vec4 v_color;
in vec2 v_uv;

out vec4 FragColor;

void main() {
    FragColor = v_color * texture(tex, v_uv);
}


