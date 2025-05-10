import glfw
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.input import Input
from core.utils.timer import Timer
from core.utils.fps import FPS
import OpenGL.GL as gl
import pygame as pg

""" 
        Base class for all applications.
        This class handles the initialization of GLFW,
        the creation of a window, and the main loop.
        It also provides a method for updating the application
        state and rendering the scene.
        Derived classes should implement the update method
        to provide their own application logic.
"""
class Base:
    """     
        Args:
            title (str): The title of the window.
            major_version (int): The major version of OpenGL to use.
            minor_version (int): The minor version of OpenGL to use.
    """
    def __init__(self, title:str = "My App", major_version:int = 3, minor_version:int =3) -> None:
        # Initialize pygame used for image loading and other utilities
        pg.init()

        # Initialize GLFW
        self._init_glfw(major_version, minor_version)
        
        # Create a windowed mode window and its OpenGL context
        self._init_window(title)

        # initialize class variables
        self._init_vars()
        
        # setup callbacks for window events
        self.input_handler.set_callbacks(self.window)

        # set resize callbacl for window
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)
        
        # set the background color
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)  

    """
        Initializes GLFW with the given OpenGL version.
        Args:
            major_version (int): The major version of OpenGL to use.
            minor_version (int): The minor version of OpenGL to use.
            Raises:
                Exception: If GLFW could not be initialized.
    """

    def _init_glfw(self,minor_version:int,major_version:int) -> None:
        # initialize GLFW and raise exception if it fails
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")

        # Set the window hints for OpenGL version
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    """
        Initializes the GLFW window with the given title.
        Args:
            title (str): The title of the window.
        Raises:
            Exception: If the GLFW window could not be created.
    """
    def _init_window(self, title:str) -> None:
        self.window_width = SCREEN_WIDTH
        self.window_height = SCREEN_HEIGHT

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(self.window_width,self.window_height, title, None, None)

        # set initial veiwport
        gl.glViewport(0, 0, self.window_width, self.window_height)
        
        # store title incase of FPS counter
        self.title = title
        
        # Check if the window was created successfully 
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)

        # Enable V-Sync
        glfw.swap_interval(1)


    """
            Initializes the variables used in the application.
            This function is called in the constructor.
            It is not necessary to call this function manually.
    """
    def _init_vars(self) -> None:
        #  core app variables
        self.timer = Timer()
        self.fps_counter = FPS() 
        self.show_fps = True
        self.input_handler = Input()


    """
        Derived classes should implement this function to update
        the application state, render the scene, and handle input.
    """
    def update(self):
        pass

    """
            Run function of an application.
            derived classes need not to implement this function.
            Unless they wish to extend this function and add their own logic.
    """
    def run(self) -> None:
        # main loop for all applications
        while not glfw.window_should_close(self.window):
            # update to be implemented in derived classes
            self.update()
           
            #swap buffers
            glfw.swap_buffers(self.window)

            # poll events
            self.input_handler.update()

            # check for quit
            if self.input_handler.quit:
                break
            
            # add FPS counter to the window title
            if self.show_fps:
                self._display_fps()

    """   
        Calculates the frames per second (FPS) and displays it in the window title. 
    """
    def _display_fps(self) -> None:
            glfw.set_window_title(self.window, self.title + f"- FPS: {self.fps_counter.update():.2f}")

    """
        Quits the application by destroying the window and terminating GLFW.
        It cleans up the resources used by the application.
        It is called automatically when the object is deleted.
        It is also called in the run method when the user quits the application.
        It is not necessary to call this method manually.
    """
    def quit(self) -> None:
        if self.window:
            glfw.destroy_window(self.window)
            self.window = None
        
        if glfw:
            glfw.terminate()
    
    """
        Destructor for the Base class.
        Cleans up the resources used by the application.
        It is called automatically when the object is deleted.
    """
    def __del__(self) -> None:
        self.quit()

    """
        Callback function for window resize events.
        This function is called when the window is resized.
        It adjusts the OpenGL viewport to match the new window size.
        Args:
            window: The GLFW window that was resized.
            width (int): The new width of the window.
            height (int): The new height of the window."""
    def _on_resize(self, window, width, height) -> None:
        gl.glViewport(0, 0, width, height)
        self.window_width = width
        self.window_height = height
