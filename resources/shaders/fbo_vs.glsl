#version 400 core

#define MAX_LIGHTS 2

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 textureCoordinates;

uniform mat4 transformationMatrix;	// the entity's position relative to the world [-1 1 1 -1]
uniform mat4 projectionMatrix;		// transform's everything into a viewing frustum (farther away in -z the smaller everything gets foreshortening)
uniform mat4 viewMatrix;			// camera's perspective

void main() {

	vec4 worldPosition = transformationMatrix * vec4(in_position, 1.0); // position is the position of the current vertex

	vec4 positionRelativeToCam = viewMatrix * worldPosition;
	gl_Position = projectionMatrix * positionRelativeToCam;
//	pass_textureCoordinates = (in_texcoord_0 / numberOfRows) + offset;
	textureCoordinates = in_texcoord_0;

}