#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D second_texture;

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates

// light dir, in world coordinates
uniform vec3 light_dir;

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
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec4 phong = vec4(k_a + k_d * max(0, dot(n, l)) + k_s * pow(max(0, dot(r, v)), s*128), 1);
    vec4 color = texture(diffuse_map, frag_tex_coords);
    vec4 color2 = texture(second_texture, frag_tex_coords);

    out_color = phong;
}
