#version 400 core

#define MAX_LIGHTS 2

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 textureCoordinates;
out vec3 surfaceNormal;
out vec3 toLightVector[MAX_LIGHTS];
out vec3 toCameraVector;
out float visibility;
out float clipDistance;

uniform mat4 transformationMatrix;	// the entity's position relative to the world [-1 1 1 -1]
uniform mat4 projectionMatrix;		// transform's everything into a viewing frustum (farther away in -z the smaller everything gets foreshortening)
uniform mat4 viewMatrix;			// camera's perspective
uniform vec3 lightPosition[MAX_LIGHTS];		// location of the light source (only one source of light so far)
uniform float useFakeLighting;

//uniform float numberOfRows;			// allows having multiple textures in the same file
//uniform vec2 offset;				// allows having multiple textures in the same file

const float density = 0.0035;
const float gradient = 5.0;

uniform vec4 plane;

void main() {

	vec4 worldPosition = transformationMatrix * vec4(in_position, 1.0); // position is the position of the current vertex

	clipDistance = dot(worldPosition, plane);

	vec4 positionRelativeToCam = viewMatrix * worldPosition;
	gl_Position = projectionMatrix * positionRelativeToCam;
//	pass_textureCoordinates = (in_texcoord_0 / numberOfRows) + offset;
	textureCoordinates = in_texcoord_0;

	vec3 actualNormal = in_normal;
	if (useFakeLighting > 0.5){
		actualNormal = vec3(0.0, 1.0, 0.0);
	}
	surfaceNormal = (transformationMatrix * vec4(actualNormal, 0.0)).xyz; //(swizzle it) convert from vec4 back to vec3
	//vec3 lightPosition2 = (transformationMatrix * vec4(lightPosition, 0.0)).xyz; //this will make the light source travel with the entity
	for (int i = 0; i < MAX_LIGHTS; i++) {
		toLightVector[i] = lightPosition[i] - worldPosition.xyz;
	}
	toCameraVector = (inverse(viewMatrix) * vec4(0.0,0.0,0.0,1.0)).xyz - worldPosition.xyz;

	float distance = length(positionRelativeToCam.xyz);
	visibility = exp(-pow((distance*density), gradient));
	visibility = clamp(visibility, 0.0, 1.0);
}