#version 400 core

#define MAX_LIGHTS 2

in vec2 textureCoordinates;

out vec4 fragColor;

uniform sampler2D texture0;

void main(){
	fragColor = texture(texture0, textureCoordinates);
}

