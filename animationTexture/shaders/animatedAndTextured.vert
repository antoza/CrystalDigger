#version 330 core

// ---- camera geometry
uniform mat4 projection, view, model;

// ---- skinning globals and attributes
const int MAX_VERTEX_BONES=4, MAX_BONES=128;
uniform mat4 bone_matrix[MAX_BONES];

// ---- vertex attributes
in vec3 position;
in vec3 normal;
in vec4 bone_ids;
in vec4 bone_weights;
in vec2 tex_coord;

out vec2 frag_tex_coords;
out vec3 w_position, w_normal;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;

void main() {
    mat4 skin_matrix = mat4(0.0);
    for(int i=0; i<MAX_VERTEX_BONES; i++) {
        skin_matrix += bone_weights[i] * bone_matrix[int(bone_ids[i])];
    }

    vec4 w_position4 = skin_matrix * vec4(position, 1.0);

    gl_Position = projection * view * model * w_position4;

    // fragment position in world coordinates
    w_position = w_position4.xyz / w_position4.w;  // dehomogenize

    // fragment normal in world coordinates
    mat3 nit_matrix = transpose(inverse(mat3(model)));
    w_normal = normalize(nit_matrix * normal);

    frag_tex_coords = tex_coord;
}
