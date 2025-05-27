from meshes.mesh import Mesh
from core.physics.collision import CollisionType,Collider,SphereCollider,BoxCollider
from geometry.simple3D.sphere import Sphere
from geometry.simple3D.box import BoxGeometry
from geometry.geometry import Geometry

class PhysicsObject:

    """
    A class representing a physics object in a 3D environment.
    stores a mesh, mass, velocity, and position of the object.
    As well as a function to handle collisions with other objects.
    """

    def __init__(self, mesh: Mesh = None, mass:int=1, velocity=[0, 0, 0], collider_Type:CollisionType = CollisionType.NONE):
        """
        Initializes the PhysicsObject with the given mesh, mass, and position.

        :param mesh: The mesh of the object.
        :param mass: The mass of the object.
        :param position: The initial position of the object in 3D space.
        """

        self._mesh = mesh
        self._mass = mass
        self._velocity = velocity
        self._collider =  self._init_collider(collider_Type)

    def _init_collider(self, collider_type:CollisionType):
        """
        Initializes the collider based on the collision type.
        :param collider_type: The type of collider to initialize.
        :return: An instance of the appropriate collider class.
        """ 
        if not self._mesh:
            raise ValueError("Mesh is not initialized. Cannot create collider without a mesh.")
        
        # if the collider type is a sphere, create a sphere collider
        if collider_type == CollisionType.SPHERE:
            return SphereCollider(self._mesh.geometry.radius,self._mesh.local_position,[self._mesh.rotation_x,self._mesh.rotation_y,self._mesh.rotation_z])
        
        # if the collider type is a box, create a box collider
        elif collider_type == CollisionType.BOX:
            return BoxCollider(self._mesh.geometry.width, self._mesh.geometry.height, self._mesh.geometry.depth,
                            self._mesh.local_position,[self._mesh.rotation_x,self._mesh.rotation_y,self._mesh.rotation_z])
        else:
            return Collider(CollisionType.NONE)

    @property
    def mesh(self):
        """
        Returns the mesh of the physics object.
        """
        return self._mesh
    
    @property
    def mass(self):
        """
        Returns the mass of the physics object.
        """
        return self._mass
    
    @mass.setter
    def mass(self, mass):
        """
        Sets the mass of the physics object.
        """
        self._mass = mass
    
    @property
    def velocity(self):
        """
        Returns the velocity of the physics object.
        """
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity):
        """
        Sets the velocity of the physics object.
        """
        self._velocity = velocity
    
    @property
    def position(self):
        """
        Returns the position of the physics object.
        """
        return self._mesh.local_position
    
    @position.setter
    def position(self, position):
        """
        Sets the position of the physics object.
        """
        if self._mesh:
            self._mesh.local_position = position
        else:
            raise ValueError("Mesh is not initialized.")
    
    @property
    def collider(self):
        """
        Returns the collision function of the physics object.
        """
        return self._collider
    
    @collider.setter
    def collider(self, collider:Collider):
        """
        Sets the collision function of the physics object.
        """
        self._collider = collider


    def change_geometry(self, geometry,collider_type:CollisionType = CollisionType.NONE):
            """
            Changes the geometry of the mesh.

            :param geometry: The new geometry to set for the mesh.
            """
            if self._mesh:
                self._mesh.geometry = geometry
                self._collider = self._init_collider(collider_type)
            else:
                raise ValueError("Mesh is not initialized.")


    def change_material(self, material):
        """
        Changes the material of the mesh.

        :param material: The new material to set for the mesh.
        """
        if self._mesh:
            self._mesh.material = material
        else:
            raise ValueError("Mesh is not initialized.")
        


    def transform(self,matrix):
        """
        Applies a transformation matrix to the mesh's geometry.

        :param matrix: The transformation matrix to apply.
        """
        if self._mesh:
            self._mesh.apply_matrix(matrix)
        else:
            raise ValueError("Mesh is not initialized.")
        