#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
in vec3 w_position, w_normal;

// light dir, in world coordinates
uniform vec3 lights[10];
uniform int nb_lights;

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

void main() {
    vec3 light_color = vec3(1, .5, 0);
    vec3 n = normalize(w_normal);
    vec3 v = normalize(w_camera_position - w_position);
    vec4 phong = vec4(0, 0, 0, 1);
    bool illuminated = false;

    for(int i=0; i < nb_lights; i++) {
        float d_sq = dot(w_position - lights[i], w_position - lights[i]);

        if(d_sq < 4) {
            illuminated = true;
            vec3 l = normalize(w_position - lights[i]);
            vec3 r = reflect(-l, n);

            vec3 diffuse_color = k_d * max(0, dot(n, l));
            vec3 specular_color = k_s * pow(max(0, dot(r, v)), s);
            phong += vec4((diffuse_color + specular_color) / d_sq, 1);
        }

        if(illuminated) phong += vec4(k_a * light_color, 1);
    }

    out_color = phong;
}