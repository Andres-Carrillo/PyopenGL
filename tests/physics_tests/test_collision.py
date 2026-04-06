"""
Unit tests for collision detection and response.

These tests verify the math directly — no app, no renderer, no OpenGL context needed.
Each test has a clear arrange / act / assert structure:
    - Arrange: set up entities at known positions
    - Act:     call the function under test
    - Assert:  check the result against expected values

Run with:
    python -m pytest tests/physics_tests/test_collision.py -v
"""

import pathlib
import sys

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

import numpy as np
import pytest

from engine.ecs.entity import Entity
from engine.ecs.components.types import COMPTYPE
from engine.ecs.components.collision import CollisionType
from engine.ecs.components.components import CollisionComponent, PhysicsBody
from engine.ecs.systems.collision import (
    sphere_vs_sphere,
    aabb_vs_aabb,
    sphere_vs_aabb,
    impulse,
    Contact,
    CollisionSystem,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_sphere(position, radius=1.0, mass=1.0, velocity=None, static=False):
    """Create an entity with a sphere collider and optional physics body."""
    e = Entity()
    e.set_position(position)
    e.add_component(COMPTYPE.COLLIDER, CollisionComponent(
        shape=CollisionType.SPHERE,
        radius=radius
    ))
    body_mass = 0.0 if static else mass
    e.add_component(COMPTYPE.PHYSICS, PhysicsBody(
        mass=body_mass,
        velocity=np.array(velocity or [0.0, 0.0, 0.0], dtype=np.float64)
    ))
    return e


def make_box(position, width=2.0, height=2.0, depth=2.0, mass=1.0, velocity=None, static=False):
    """Create an entity with a box collider and optional physics body."""
    e = Entity()
    e.set_position(position)
    e.add_component(COMPTYPE.COLLIDER, CollisionComponent(
        shape=CollisionType.BOX,
        width=width,
        height=height,
        depth=depth
    ))
    body_mass = 0.0 if static else mass
    e.add_component(COMPTYPE.PHYSICS, PhysicsBody(
        mass=body_mass,
        velocity=np.array(velocity or [0.0, 0.0, 0.0], dtype=np.float64)
    ))
    return e


# ---------------------------------------------------------------------------
# sphere_vs_sphere
# ---------------------------------------------------------------------------

class TestSphereVsSphere:

    def test_overlapping_returns_contact(self):
        # Two unit spheres 1.5 apart — overlap of 0.5
        a = make_sphere([0, 0, 0], radius=1.0)
        b = make_sphere([1.5, 0, 0], radius=1.0)

        contact = sphere_vs_sphere(a, b)

        assert contact is not None

    def test_penetration_depth_correct(self):
        a = make_sphere([0, 0, 0], radius=1.0)
        b = make_sphere([1.5, 0, 0], radius=1.0)

        contact = sphere_vs_sphere(a, b)

        assert abs(contact.penetration - 0.5) < 1e-6

    def test_normal_points_from_b_to_a(self):
        # a is to the right of b → normal should point in +X
        a = make_sphere([1.5, 0, 0], radius=1.0)
        b = make_sphere([0,   0, 0], radius=1.0)

        contact = sphere_vs_sphere(a, b)

        assert np.allclose(contact.normal, [1, 0, 0], atol=1e-6)

    def test_separated_returns_none(self):
        a = make_sphere([0, 0, 0], radius=1.0)
        b = make_sphere([5, 0, 0], radius=1.0)

        assert sphere_vs_sphere(a, b) is None

    def test_exactly_touching_returns_none(self):
        # Distance exactly equals sum of radii — touching, not overlapping
        a = make_sphere([0, 0, 0], radius=1.0)
        b = make_sphere([2, 0, 0], radius=1.0)

        assert sphere_vs_sphere(a, b) is None

    def test_different_radii(self):
        a = make_sphere([0, 0, 0], radius=2.0)
        b = make_sphere([2.5, 0, 0], radius=1.0)  # sum=3, dist=2.5 → overlap=0.5

        contact = sphere_vs_sphere(a, b)

        assert contact is not None
        assert abs(contact.penetration - 0.5) < 1e-6

    def test_contact_entities_assigned_correctly(self):
        a = make_sphere([0, 0, 0])
        b = make_sphere([1, 0, 0])

        contact = sphere_vs_sphere(a, b)

        assert contact.entity_a is a
        assert contact.entity_b is b

    def test_overlapping_centers_uses_fallback_normal(self):
        # Perfectly overlapping — distance == 0, should use [0,1,0] fallback
        a = make_sphere([0, 0, 0], radius=1.0)
        b = make_sphere([0, 0, 0], radius=1.0)

        contact = sphere_vs_sphere(a, b)

        assert contact is not None
        assert np.allclose(contact.normal, [0, 1, 0], atol=1e-6)


# ---------------------------------------------------------------------------
# aabb_vs_aabb
# ---------------------------------------------------------------------------

class TestAabbVsAabb:

    def test_overlapping_returns_contact(self):
        # Two 2x2x2 boxes, centers 1.5 apart on X — overlap of 0.5
        a = make_box([0,   0, 0], width=2, height=2, depth=2)
        b = make_box([1.5, 0, 0], width=2, height=2, depth=2)

        contact = aabb_vs_aabb(a, b)

        assert contact is not None

    def test_separated_returns_none(self):
        a = make_box([0, 0, 0], width=2, height=2, depth=2)
        b = make_box([5, 0, 0], width=2, height=2, depth=2)

        assert aabb_vs_aabb(a, b) is None

    def test_minimum_penetration_axis_is_x(self):
        # Overlap on X(0.5) is less than Y(2.0) and Z(2.0) → normal along X
        a = make_box([0,   0, 0], width=2, height=2, depth=2)
        b = make_box([1.5, 0, 0], width=2, height=2, depth=2)

        contact = aabb_vs_aabb(a, b)

        assert abs(contact.normal[1]) < 1e-6  # no Y component
        assert abs(contact.normal[2]) < 1e-6  # no Z component
        assert abs(contact.normal[0]) > 0.9   # X dominant

    def test_minimum_penetration_axis_is_y(self):
        a = make_box([0, 0,   0], width=2, height=2, depth=2)
        b = make_box([0, 1.5, 0], width=2, height=2, depth=2)

        contact = aabb_vs_aabb(a, b)

        assert abs(contact.normal[0]) < 1e-6
        assert abs(contact.normal[2]) < 1e-6
        assert abs(contact.normal[1]) > 0.9

    def test_gap_on_one_axis_returns_none(self):
        # Overlap on Y and Z but gap on X
        a = make_box([0, 0, 0], width=1, height=4, depth=4)
        b = make_box([3, 0, 0], width=1, height=4, depth=4)

        assert aabb_vs_aabb(a, b) is None


# ---------------------------------------------------------------------------
# sphere_vs_aabb
# ---------------------------------------------------------------------------

class TestSphereVsAabb:

    def test_sphere_overlapping_box_face(self):
        sphere = make_sphere([1.4, 0, 0], radius=1.0)
        box    = make_box([0, 0, 0], width=2, height=2, depth=2)

        contact = sphere_vs_aabb(sphere, box)

        assert contact is not None

    def test_sphere_outside_box_returns_none(self):
        sphere = make_sphere([5, 0, 0], radius=1.0)
        box    = make_box([0, 0, 0], width=2, height=2, depth=2)

        assert sphere_vs_aabb(sphere, box) is None

    def test_contact_point_is_on_box_surface(self):
        sphere = make_sphere([1.4, 0, 0], radius=1.0)
        box    = make_box([0, 0, 0], width=2, height=2, depth=2)

        contact = sphere_vs_aabb(sphere, box)

        # Contact point should be on the box face at x=1.0
        assert abs(contact.point[0] - 1.0) < 1e-6

    def test_sphere_inside_box_uses_fallback_normal(self):
        # Sphere fully inside box — distance to closest == 0
        sphere = make_sphere([0, 0, 0], radius=0.1)
        box    = make_box([0, 0, 0], width=4, height=4, depth=4)

        contact = sphere_vs_aabb(sphere, box)

        assert contact is not None
        assert np.allclose(contact.normal, [0, 1, 0], atol=1e-6)


# ---------------------------------------------------------------------------
# impulse()
# ---------------------------------------------------------------------------

class TestImpulse:

    def test_approaching_bodies_get_impulse(self):
        # a moving right, b moving left — head-on collision
        # normal points from b (x=1) toward a (x=0) → [-1,0,0]
        a = make_sphere([0, 0, 0], velocity=[ 1.0, 0.0, 0.0])
        b = make_sphere([1, 0, 0], velocity=[-1.0, 0.0, 0.0])

        contact = Contact(
            entity_a=a,
            entity_b=b,
            normal=np.array([-1.0, 0.0, 0.0]),
            penetration=1.0,
            point=np.array([0.5, 0.0, 0.0])
        )

        imp = impulse(contact)

        assert np.linalg.norm(imp) > 0

    def test_separating_bodies_get_zero_impulse(self):
        # a moving left, b moving right — already separating
        # normal points from b (x=1) toward a (x=0) → [-1,0,0]
        a = make_sphere([0, 0, 0], velocity=[-1.0, 0.0, 0.0])
        b = make_sphere([1, 0, 0], velocity=[ 1.0, 0.0, 0.0])

        contact = Contact(
            entity_a=a,
            entity_b=b,
            normal=np.array([-1.0, 0.0, 0.0]),
            penetration=0.1,
            point=np.array([0.5, 0.0, 0.0])
        )

        imp = impulse(contact)

        assert np.allclose(imp, [0, 0, 0])

    def test_impulse_direction_along_normal(self):
        a = make_sphere([0, 0, 0], velocity=[1.0, 0.0, 0.0])
        b = make_sphere([1, 0, 0], velocity=[0.0, 0.0, 0.0])

        contact = Contact(
            entity_a=a,
            entity_b=b,
            normal=np.array([-1.0, 0.0, 0.0]),
            penetration=0.5,
            point=np.array([0.5, 0.0, 0.0])
        )

        imp = impulse(contact)

        # Impulse should be purely along X
        assert abs(imp[1]) < 1e-6
        assert abs(imp[2]) < 1e-6

    def test_static_body_mass_zero_does_not_affect_denominator(self):
        # Static body (mass=0) — impulse should still be computed
        a = make_sphere([0, 0, 0], velocity=[1.0, 0.0, 0.0])
        b = make_sphere([1, 0, 0], static=True)

        contact = Contact(
            entity_a=a,
            entity_b=b,
            normal=np.array([-1.0, 0.0, 0.0]),
            penetration=0.5,
            point=np.array([0.5, 0.0, 0.0])
        )

        imp = impulse(contact)

        assert np.linalg.norm(imp) > 0


# ---------------------------------------------------------------------------
# CollisionSystem integration
# ---------------------------------------------------------------------------

class TestCollisionSystem:

    def test_run_detects_colliding_pair(self):
        a = make_sphere([0,   0, 0], velocity=[ 1, 0, 0])
        b = make_sphere([1.5, 0, 0], velocity=[-1, 0, 0])

        system = CollisionSystem()
        # Should not raise — verifies the full pipeline runs
        system.run([a, b])

    def test_run_ignores_separated_pair(self):
        a = make_sphere([0, 0, 0])
        b = make_sphere([9, 0, 0])

        contacts = CollisionSystem.check_collisions([a, b])

        assert len(contacts) == 0

    def test_velocity_changes_after_collision(self):
        # Two equal-mass spheres in head-on collision
        a = make_sphere([0,   0, 0], mass=1.0, velocity=[ 2, 0, 0])
        b = make_sphere([1.5, 0, 0], mass=1.0, velocity=[-2, 0, 0])

        phys_a = a.get_component(COMPTYPE.PHYSICS)
        phys_b = b.get_component(COMPTYPE.PHYSICS)

        vel_a_before = phys_a.velocity.copy()
        vel_b_before = phys_b.velocity.copy()

        CollisionSystem.run(CollisionSystem(), [a, b])

        # Velocities must have changed
        assert not np.allclose(phys_a.velocity, vel_a_before)
        assert not np.allclose(phys_b.velocity, vel_b_before)

    def test_static_body_velocity_unchanged(self):
        dynamic = make_sphere([0,   0, 0], mass=1.0, velocity=[2, 0, 0])
        static  = make_sphere([1.5, 0, 0], static=True)

        phys_static = static.get_component(COMPTYPE.PHYSICS)
        vel_before  = phys_static.velocity.copy()

        CollisionSystem.run(CollisionSystem(), [dynamic, static])

        assert np.allclose(phys_static.velocity, vel_before)
