import OpenGL.GL as gl
import numpy as np
import ctypes
from config import create_shader_program,vertex_3d

def build_triangle_mesh() -> tuple[tuple[int],int]:
    position_data = np.array(
        (-0.75,-0.75,0.0,
         0.75,-0.75,0.0,
         0.0,0.75,0.0
        ),dtype=np.float32
    )

    color_data = np.array(
        (0,1,2),dtype=np.uint32
    )

    vao = gl.glGenVertexArrays(1)

    gl.glBindVertexArray(vao)


    position_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, position_buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER,position_data.nbytes,position_data,gl.GL_STATIC_DRAW)

    attribute_index = 0
    size = 3
    stride = 12
    offset = 0
    gl.glVertexAttribPointer(attribute_index,size,gl.GL_FLOAT,gl.GL_FALSE,stride,ctypes.c_void_p(offset))

    gl.glEnableVertexAttribArray(attribute_index)



    color_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, color_buffer)

    gl.glBufferData(gl.GL_ARRAY_BUFFER,color_data.nbytes,color_data,gl.GL_STATIC_DRAW)

    attribute_index = 1
    size = 1
    stride = 4
    offset = 0
    gl.glVertexAttribIPointer(attribute_index,size,gl.GL_UNSIGNED_INT,stride,ctypes.c_void_p(offset))

    gl.glEnableVertexAttribArray(attribute_index)


    return ((position_buffer,color_buffer),vao)



def build_triangle_mesh2() -> tuple[tuple[int],int]:

    vertex_data = np.zeros(3,dtype=vertex_3d)
    vertex_data[0] = (-0.75,-0.75,0.0,0)
    vertex_data[1] = (0.75,-0.75,0.0,1)
    vertex_data[2] = (0.0,0.75,0.0,2)
    # position_data = np.array(
    #     (-0.75,-0.75,0.0,
    #      0.75,-0.75,0.0,
    #      0.0,0.75,0.0
    #     ),dtype=np.float32
    # )

    # color_data = np.array(
    #     (0,1,2),dtype=np.uint32
    # )

    vao = gl.glGenVertexArrays(1)

    gl.glBindVertexArray(vao)


    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER,vertex_data.nbytes,vertex_data,gl.GL_STATIC_DRAW)

    attribute_index = 0
    size = 3
    stride = vertex_3d.itemsize
    offset = 0
    gl.glVertexAttribPointer(attribute_index,size,gl.GL_FLOAT,gl.GL_FALSE,stride,ctypes.c_void_p(offset))

    gl.glEnableVertexAttribArray(attribute_index)

    offset += 12
    attribute_index = 1
    size = 1



    gl.glVertexAttribIPointer(attribute_index,size,gl.GL_UNSIGNED_INT,stride,ctypes.c_void_p(offset))

    gl.glEnableVertexAttribArray(attribute_index)


    return (vbo,vao)


def build_quad_mesh() -> tuple[tuple[int],int]:

    vertex_data = np.zeros(4,dtype=vertex_3d)
    vertex_data[0] = (-0.75,-0.75,0.0,0)
    vertex_data[1] = (0.75,-0.75,0.0,1)
    vertex_data[2] = (0.75,0.75,0.0,2)
    vertex_data[3] = (-0.75,0.75,0.0,1)


    index_data = np.array((0,1,2,2,3,0),dtype=np.ubyte)
    # position_data = np.array(
    #     (-0.75,-0.75,0.0,
    #      0.75,-0.75,0.0,
    #      0.0,0.75,0.0
    #     ),dtype=np.float32
    # )

    # color_data = np.array(
    #     (0,1,2),dtype=np.uint32
    # )

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)


    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER,vertex_data.nbytes,vertex_data,gl.GL_STATIC_DRAW)

    attribute_index = 0
    size = 3
    stride = vertex_3d.itemsize
    offset = 0

    gl.glVertexAttribPointer(attribute_index,size,gl.GL_FLOAT,gl.GL_FALSE,stride,ctypes.c_void_p(offset))
    gl.glEnableVertexAttribArray(attribute_index)

    offset += 12
    attribute_index = 1
    size = 1

    gl.glVertexAttribIPointer(attribute_index,size,gl.GL_UNSIGNED_INT,stride,ctypes.c_void_p(offset))
    gl.glEnableVertexAttribArray(attribute_index)

    ebo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,index_data.nbytes,index_data,gl.GL_STATIC_DRAW)

    return (ebo,vbo,vao)