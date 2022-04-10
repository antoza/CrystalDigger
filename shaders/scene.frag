#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
in vec3 w_position, w_normal;

// light spots
uniform vec3 lights[10];
uniform int nb_lights;
uniform float d_segt;

// colors for the light gradient
uniform vec3 light_colors[10];
uniform vec3 catmull[10];
uniform int nb_colors;

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

vec3 hermite_spline(float d) {

    // If the fragment is too far, it is black
    if(d >= nb_colors * d_segt)
        return vec3(0, 0, 0);

    int segment = int(d/d_segt);

    float t = (d - segment * d_segt) / d_segt;
    float t_2 = t*t;
    float t_3 = t_2*t;

    vec3 p0 = light_colors[segment];
    vec3 p1 = light_colors[segment+1];
    vec3 m0 = catmull[segment];
    vec3 m1 = catmull[segment+1];

    vec3 result = (2*t_3 - 3*t_2 + 1) * p0;
    result += (-2*t_3 + 3*t_2) * p1;
    result += (t_3 - 2*t_2 + t) * m0;
    result += (t_3 - t_2) * m1;

    return result;
}


void main() {
    vec3 n = normalize(w_normal);
    vec3 v = normalize(w_camera_position - w_position);
    vec4 phong = vec4(0, 0, 0, 1);

    for(int i=0; i < nb_lights; i++) {
        float d_sq = dot(w_position - lights[i], w_position - lights[i]);

        vec3 l = normalize(w_position - lights[i]);
        vec3 r = reflect(-l, n);

        vec3 light_color = hermite_spline(d_sq);
        vec3 diffuse_color = k_d * light_color * max(0, dot(n, l));
        vec3 specular_color = k_s * light_color * pow(max(0, dot(r, v)), s);
        phong += vec4((diffuse_color + specular_color) / d_sq, 1);
        phong += vec4(k_a * light_color, 1);
    }

    out_color = phong;
}