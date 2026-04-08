import numpy as np

class PhysicsObject:
    def __init__(self, x, y, z=0, mass=1.0, radius=20, mode="2d"):
        self.pos = np.array([x, y, z], dtype=float)
        self.vel = np.array([0.0, 0.0, 0.0])
        self.acc = np.array([0.0, 0.0, 0.0])
        self.mass = mass
        self.radius = radius
        self.mode = mode          # "2d" or "3d"
        self.trail = []           # last N positions for ghost trail
        self.max_trail = 30
        self.restitution = 0.7    # bounciness: 1.0 = perfectly elastic
        self.on_ground = False

    def apply_force(self, force):
        # F = ma  =>  a = F/m
        self.acc += force / self.mass

    def update(self, dt, gravity, friction_coeff, bounds):
        """
        dt: time step in seconds (typically 1/60)
        gravity: float, pixels/s^2 downward
        friction_coeff: float 0-1
        bounds: (width, height, depth) of the simulation space
        """
        W, H, D = bounds

        # --- Apply gravity ---
        gravity_force = np.array([0.0, gravity * self.mass, 0.0])
        self.apply_force(gravity_force)

        # --- Integrate: update velocity and position ---
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        # --- Reset acceleration for next frame ---
        self.acc = np.array([0.0, 0.0, 0.0])

        # --- Ground collision (y axis) ---
        if self.pos[1] + self.radius >= H:
            self.pos[1] = H - self.radius
            self.vel[1] *= -self.restitution      # bounce
            self.on_ground = True

            # Apply friction only when on ground
            self.vel[0] *= (1 - friction_coeff)
        else:
            self.on_ground = False

        # --- Wall collisions (x axis) ---
        if self.pos[0] - self.radius <= 0:
            self.pos[0] = self.radius
            self.vel[0] *= -self.restitution
        elif self.pos[0] + self.radius >= W:
            self.pos[0] = W - self.radius
            self.vel[0] *= -self.restitution

        # --- Depth collisions (z axis, only matters in 3D) ---
        if self.mode == "3d":
            if self.pos[2] - self.radius <= -D/2:
                self.pos[2] = -D/2 + self.radius
                self.vel[2] *= -self.restitution
            elif self.pos[2] + self.radius >= D/2:
                self.pos[2] = D/2 - self.radius
                self.vel[2] *= -self.restitution

        # --- Store trail ---
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

    def kinetic_energy(self):
        speed_sq = np.dot(self.vel, self.vel)
        return 0.5 * self.mass * speed_sq

    def potential_energy(self, ground_y, gravity):
        height = ground_y - self.pos[1]   # pixels above ground
        return self.mass * gravity * max(height, 0)

    def momentum(self):
        return self.mass * self.vel


class PhysicsEngine:
    def __init__(self, width, height, depth=500):
        self.objects = []
        self.gravity = 500.0        # pixels/s^2
        self.friction = 0.08
        self.bounds = (width, height, depth)
        self.paused = False
        self.mode = "2d"            # or "3d"

    def spawn(self, x, y, z=0):
        obj = PhysicsObject(x, y, z, mode=self.mode)
        self.objects.append(obj)
        return obj

    def delete_nearest(self, x, y):
        if not self.objects:
            return
        nearest = min(self.objects,
                      key=lambda o: (o.pos[0]-x)**2 + (o.pos[1]-y)**2)
        self.objects.remove(nearest)

    def update(self, dt):
        if self.paused:
            return
        for obj in self.objects:
            obj.mode = self.mode
            obj.update(dt, self.gravity, self.friction, self.bounds)

        # Object vs object collisions
        for i in range(len(self.objects)):
            for j in range(i+1, len(self.objects)):
                self._resolve_collision(self.objects[i], self.objects[j])

    def _resolve_collision(self, a, b):
        diff = a.pos - b.pos
        dist = np.linalg.norm(diff)
        min_dist = a.radius + b.radius

        if dist < min_dist and dist > 0:
            # Push objects apart
            normal = diff / dist
            overlap = min_dist - dist
            a.pos += normal * overlap * 0.5
            b.pos -= normal * overlap * 0.5

            # Exchange momentum along collision normal (1D elastic collision)
            rel_vel = a.vel - b.vel
            speed = np.dot(rel_vel, normal)
            if speed < 0:   # only resolve if moving toward each other
                impulse = (2 * speed) / (a.mass + b.mass)
                a.vel -= impulse * b.mass * normal
                b.vel += impulse * a.mass * normal

    def toggle_mode(self):
        self.mode = "3d" if self.mode == "2d" else "2d"
        print(f"Switched to {self.mode} mode")