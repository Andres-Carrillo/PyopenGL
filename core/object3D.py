import numpy as np
from core.utils.matrix import Matrix


class Object3D:
    """ Represent a node in the scene graph tree structure """
    def __init__(self):
        # local transform matrix with respect to the parent of the object
        self._matrix = Matrix.mat4_identity()
        self._parent = None
        self._children_list = []

    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        if not isinstance(other, Object3D):
            return False
        return id(self) == id(other)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def id(self):
        """ Return the id of the object """
        return id(self)

    @property
    def children_list(self):
        return self._children_list

    @children_list.setter
    def children_list(self, children_list):
        self._children_list = children_list

    @property
    def descendant_list(self):
        """ Return a single list containing all descendants """
        # master list of all descendant nodes
        descendant_list = []
        # nodes to be added to descendant list,
        # and whose children will be added to this list
        nodes_to_process = [self]
        # continue processing nodes while any are left
        while len(nodes_to_process) > 0:
            # remove first node from list
            node = nodes_to_process.pop(0)
            # add this node to descendant list
            descendant_list.append(node)
            # children of this node must also be processed
            nodes_to_process = node._children_list + nodes_to_process
        return descendant_list

    @property
    def global_matrix(self):
        """
        Calculate the transformation of this Object3D
        relative to the root Object3D of the scene graph
        """
        if self._parent is None:
            return self._matrix
        else:
            return self._parent.global_matrix @ self._matrix

    @property
    def global_position(self):
        """ Return the global or world position of the object """
        return [self.global_matrix.item((0, 3)),
                self.global_matrix.item((1, 3)),
                self.global_matrix.item((2, 3))]

    @property
    def local_matrix(self):
        return self._matrix

    @local_matrix.setter
    def local_matrix(self, matrix):
        self._matrix = matrix

    @property
    def rotation_x(self):
        return np.arctan2(self._matrix[2, 1], self._matrix[2, 2])
    
    @property
    def rotation_y(self):
        return np.arctan2(-self._matrix[2, 0], np.sqrt(self._matrix[2, 1]**2 + self._matrix[2, 2]**2))
    
    @property
    def rotation_z(self):
        return np.arctan2(self._matrix[1, 0], self._matrix[0, 0])

    @property
    def local_position(self):
        """
        Return the local position of the object (with respect to its parent)
        """
        # The position of an object can be determined from entries in the
        # last column of the transform matrix
        return [self._matrix.item((0, 3)),
                self._matrix.item((1, 3)),
                self._matrix.item((2, 3))]

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def rotation_matrix(self):
        """
        Returns 3x3 submatrix with rotation data.
        3x3 top-left submatrix contains only rotation data.
        """
        return np.array(
            [self._matrix[0][0:3],
             self._matrix[1][0:3],
             self._matrix[2][0:3]]
        ).astype(float)

    @property
    def direction(self):
        forward = np.array([0, 0, -1]).astype(float)
        return list(self.rotation_matrix @ forward)
    
    @property
    def ueler_angles(self):
        """
        Returns the Euler angles (in radians) of the object.
        The angles are in the order of rotation around X, Y, and Z axes.
        """
        return np.array([self.rotation_x, self.rotation_y, self.rotation_z])

    def add(self, child):
        self._children_list.append(child)
        child.parent = self

    def remove(self, child):
        self._children_list.remove(child)
        child.parent = None

    # apply geometric transformations
    def apply_matrix(self, matrix, local=True):
        if local:
            # local transform
            self._matrix = self._matrix @ matrix
        else:
            # global transform
            self._matrix = matrix @ self._matrix

    def translate(self, x, y, z, local=True):
        m = Matrix.mat4_translation(x, y, z)
        self.apply_matrix(m, local)


    def rotate_xyz(self, angles, local=True):
        """
        Rotate the object around X, Y, and Z axes by the given angles (in radians).
        angles: [angle_x, angle_y, angle_z]
        """
        m_x = Matrix.mat4_rotate_x(angles[0])
        m_y = Matrix.mat4_rotate_y(angles[1])
        m_z = Matrix.mat4_rotate_z(angles[2])

        # print(f"X: {angles[0]}, Y: {angles[1]}, Z: {angles[2]}")
        # print(f"m_x: {m_x}")
        # print(f"m_y: {m_y}")
        # print(f"m_z: {m_z}")
        # Combine rotations: X, then Y, then Z (order can be changed as needed)
        rotation_matrix =  m_x @ m_y @ m_z
        self.apply_matrix(rotation_matrix, local)


    def matrix_to_euler_xyz(self,R):
        """
        Convert a 3x3 or 4x4 rotation matrix to Euler angles (XYZ order).
        Returns angles in radians: [x, y, z]
        """
        if R.shape == (4, 4):
            R = R[:3, :3]
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
        z = np.arctan2(R[1, 0], R[0, 0])
        return np.array([x, y, z])

    def rotate_x(self, angle, local=True):
        m = Matrix.mat4_rotate_x(angle)
        self.apply_matrix(m, local)

    def rotate_y(self, angle, local=True):
        m = Matrix.mat4_rotate_y(angle)
        self.apply_matrix(m, local)

    def rotate_z(self, angle, local=True):
        m = Matrix.mat4_rotate_z(angle)
        self.apply_matrix(m, local)

    def scale(self, s, local=True):
        m = Matrix.mat4_scale_uniform(s)
        self.apply_matrix(m, local)

    def set_position(self, position):
        """ Set the local position of the object """
        self._matrix[0, 3] = position[0]
        self._matrix[1, 3] = position[1]
        self._matrix[2, 3] = position[2]
        # self._matrix.itemset((1, 3), position[1])
        # self._matrix.itemset((2, 3), position[2])

    def look_at(self, target_position):
        self._matrix = Matrix.make_look_at(self.global_position, target_position)

    def set_direction(self, direction):
        position = self.local_position
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2]
        ]
        self.look_at(target_position)


    def set_euler_rotation(self, rotation):
        """
        Set the local rotation of the object using Euler angles (in radians).
        rotation: [angle_x, angle_y, angle_z]
        """
        self.rotate_xyz(rotation, local=True)

    
    def update_euler_from_matrix(self):
        self.euler_angles = self.matrix_to_euler_xyz(self.rotation_matrix)
