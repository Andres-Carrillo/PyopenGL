import OpenGL.GL as gl
import pygame as pg

class Texture(object):
    def __init__(self,image_path:str = None,properties:dict = {}) -> None:
        # Texture surface will be pygame object for handling images
        self.texture_surface = None

        # Texture reference from GPU setup through OpenGL
        self.texture_reference = gl.glGenTextures(1)

        # Default properties for texture
        self.properties = {
            "magnify_filter":gl.GL_LINEAR,
            "minify_filter":gl.GL_LINEAR_MIPMAP_LINEAR,
            "wrap":gl.GL_REPEAT,
        }

        # update properties with user defined properties
        self.set_properties(properties)

        if image_path is not None:
            # Load the image file
            self.load_texture_img(image_path)            
            # upload the texture to GPU
            self.upload_texture()


    def set_properties(self,properties:dict) -> None:
        """
        Set the properties of the texture.
        """
        for key,data in properties.items():
            if key in self.properties:
                self.properties[key] = data
            else:
                raise Exception("Warning: " + key + " is not a valid Texture Property.")
            

    def load_texture_img(self,image_path:str) -> None:
        print(f"Loading texture from {image_path}")
        self.surface = pg.image.load(image_path)

        if self.surface is None:
            raise RuntimeError(f"Could not load image {image_path}")


    def upload_texture(self) -> None:
        width = self.surface.get_width()
        height = self.surface.get_height()

        print(f"Texture size: {width} x {height}")

        #convert texture image to string buffer:
        pixel_data = pg.image.tostring(self.surface,"RGBA",True)

        # bind the texture to the GPU
        gl.glBindTexture(gl.GL_TEXTURE_2D,self.texture_reference)

        # send the texture data to the GPU
        gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,width,height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,pixel_data)

        #generate Mipmaps of texture
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        # set magnification filter
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,self.properties["magnify_filter"])
        # set minification filter
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,self.properties["minify_filter"])


        # set wrap mode
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,self.properties["wrap"])
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,self.properties["wrap"])


        # set border color to white:
        gl.glTexParameterfv(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_BORDER_COLOR,[1.0,1.0,1.0,1.0])



                

