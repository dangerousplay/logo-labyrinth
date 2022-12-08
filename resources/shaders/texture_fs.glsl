#version 400 core

#define MAX_LIGHTS 2

in vec2 textureCoordinates;
in vec3 surfaceNormal;
in vec3 toLightVector[MAX_LIGHTS];
in vec3 toCameraVector;
in float visibility;
in float clipDistance;

out vec4 fragColor;

uniform sampler2D texture0;
uniform vec3 lightColour[MAX_LIGHTS];		//light source's color (which can change over time)
uniform vec3 attenuation[MAX_LIGHTS];		//one for each light source
uniform float shineDamper;
uniform float reflectivity;
const vec3 skyColor = vec3(0.5444, 0.62, 0.69);

void main(){

	vec3 unitNormal  = normalize(surfaceNormal);
	vec3 unitVectorToCamera = normalize(toCameraVector);

	vec3 totalDiffuse = vec3(0.0);
	vec3 totalSpecular = vec3(0.0);

	for (int i = 0; i < MAX_LIGHTS; i++){
		float distance = length(toLightVector[i]);
		float attenuationFactor = attenuation[i].x + (attenuation[i].y * distance) + (attenuation[i].z * distance * distance);
		vec3 unitLightVector = normalize(toLightVector[i]);  // pointing from the surface to the light source
		float nDot1 = dot(unitNormal, unitLightVector);
		float brightness = max(nDot1, 0.0);
		vec3 lightDirection = -unitLightVector; 		  // pointing from the light source to the surface
		vec3 reflectedLightDirection = reflect(lightDirection, unitNormal);
		float specularFactor = dot(reflectedLightDirection, unitVectorToCamera);
		specularFactor = max(specularFactor, 0.0);

		float dampedFactor = pow(specularFactor, shineDamper);
		totalDiffuse = totalDiffuse + (brightness*lightColour[i])/attenuationFactor;
		totalSpecular = totalSpecular + (dampedFactor * reflectivity * lightColour[i])/attenuationFactor;
	}

	totalDiffuse = max(totalDiffuse, 0.1);

	vec4 textureColour = texture(texture0,textureCoordinates);

	fragColor = vec4(totalDiffuse, 1.0) * textureColour;
    fragColor = mix(vec4(skyColor, 1.0), fragColor, 1);  // mix the skyColor with the current out_Color, by the visibility gradient.
}

