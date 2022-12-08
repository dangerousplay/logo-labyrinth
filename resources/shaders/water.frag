#version 400 core

in vec4 clipSpace;
in vec2 textureCoords;
in vec3 toCameraVector;
in vec3 fromLightVector;

out vec4 out_Color;

uniform sampler2D reflectionTexture;
uniform sampler2D refractionTexture;
uniform sampler2D dudvMap;
uniform sampler2D normalMap;
uniform sampler2D depthMap;
uniform vec3 lightColour;

uniform float moveFactor;

const float waveStrength = 0.04;
const float shineDamper = 20.0;
const float reflectivity = 0.5;

void main(void) {

	// reflection/refraction coordinates
	vec2 ndc = (clipSpace.xy/clipSpace.w)/2.0 + 0.5;
	vec2 refractTexCoords = vec2(ndc.x, ndc.y);
	vec2 reflectTexCoords = vec2(ndc.x, -ndc.y);
	// reflection/refraction coordinates

	// compute the depth of the water
	float near = 0.1;
	float far = 3500.0;

	float depth = texture(depthMap, refractTexCoords).r; // this is where the depth info is stored from 0-1; But it is not linear because of the near and far plane!
	float floorDistance = 2.0 * near * far / (far + near - (2.0 * depth - 1.0) * (far - near));

	depth = gl_FragCoord.z; // grab the distance from the camera to the surface height of the water and linearize it the same way as above for the distance of the camera to the water bottom
	float waterDistance = 2.0 * near * far / (far + near - (2.0 * depth - 1.0) * (far - near));
	float waterDepth = floorDistance - waterDistance;

	// compute the depth of the water

	// wave distortion
	vec2 distortedTexCoords = texture(dudvMap, vec2(textureCoords.x + moveFactor, textureCoords.y)).rg * 0.1;
	distortedTexCoords = textureCoords + vec2(distortedTexCoords.x, distortedTexCoords.y+moveFactor);
	vec2 totalDistortion = (texture(dudvMap, distortedTexCoords).rg * 2.0 - 1.0) * waveStrength * clamp(waterDepth/20.0, 0.0, 1.0);
	// wave distortion

	// edges
	refractTexCoords += totalDistortion;
	refractTexCoords = clamp(refractTexCoords, 0.001, 0.999);

	reflectTexCoords += totalDistortion;
	reflectTexCoords.x = clamp(reflectTexCoords.x, 0.001, 0.999);
	reflectTexCoords.y = clamp(reflectTexCoords.y, -0.999, -0.001);
	// edges

	vec4 normalMapColour = texture(normalMap, distortedTexCoords);
	vec3 unitNormal = vec3(normalMapColour.r * 2.0 - 1.0, normalMapColour.b * 5.0, normalMapColour.g * 2.0 - 1.0);
	unitNormal = normalize(unitNormal);

	// Fresnel effect
	vec4 reflectionColour = texture(reflectionTexture, reflectTexCoords);
	vec4 refractionColour = texture(refractionTexture, refractTexCoords);

	vec3 unitVectorToCamera = normalize(toCameraVector);
	float refractiveFactor = dot(unitVectorToCamera, unitNormal);
	refractiveFactor = pow(refractiveFactor, 0.5);
	// Fresnel effect

	// specular lighting on the water (same as episode 12)
	vec3 reflectedLightDirection = reflect(normalize(fromLightVector), unitNormal);
	float specularFactor = dot(reflectedLightDirection, unitVectorToCamera);
	specularFactor = max(specularFactor, 0.0);
	float dampedFactor = pow(specularFactor, shineDamper);
	vec3 specularHighLights = lightColour * dampedFactor * reflectivity;
	// specular lighting on the water


	out_Color = mix(reflectionColour, refractionColour, refractiveFactor); // finish Fresnel
	out_Color = mix(out_Color, vec4(0.0, 0.3, 0.5, 1.0), 0.2) + vec4(specularHighLights, 0.0); // miz with a blue tint and specular lights
	out_Color.a = clamp(waterDepth/5.0, 0.0, 1.0);
}