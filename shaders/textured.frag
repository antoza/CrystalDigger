#version 330 core

uniform sampler2D diffuse_map;

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    vec3 light = vec3(0, 0, -1);
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = 2*k_d * max(0, dot(n, l));
    vec3 specular_color = k_s * pow(max(0, dot(r, v)), s*128);
    vec4 phong = vec4(k_a + diffuse_color + specular_color, 1);

    vec4 color = texture(diffuse_map, frag_tex_coords);
    if((color.x + color.y) < color.z)
        color += vec4(0.5, 0, 0.3, 1);
    out_color = color * phong;
}
