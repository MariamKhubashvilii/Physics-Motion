import cv2
import numpy as np

class Renderer:
    def __init__(self, width, height, depth=500):
        self.W = width
        self.H = height
        self.D = depth
        # Perspective projection vanishing point
        self.fov = 500   # focal length in pixels

    def project_3d(self, x, y, z):
        """
        Simple perspective projection.
        z=0 means center depth, negative z = closer to camera.
        Returns (screen_x, screen_y, scale)
        """
        z_shifted = z + self.fov
        if z_shifted <= 0:
            z_shifted = 0.001
        scale = self.fov / z_shifted
        sx = int(self.W/2 + (x - self.W/2) * scale)
        sy = int(self.H/2 + (y - self.H/2) * scale)
        return sx, sy, scale

    def draw_objects(self, frame, objects, mode):
        for obj in objects:
            self._draw_trail(frame, obj, mode)
            self._draw_object(frame, obj, mode)
            self._draw_vectors(frame, obj, mode)
            self._draw_stats(frame, obj, mode)

    def _draw_trail(self, frame, obj, mode):
        for i, pos in enumerate(obj.trail):
            alpha = i / len(obj.trail)   # fade older positions
            color = (int(255*alpha), int(100*alpha), 255)
            if mode == "3d":
                sx, sy, _ = self.project_3d(*pos)
            else:
                sx, sy = int(pos[0]), int(pos[1])
            radius = max(2, int(4 * alpha))
            cv2.circle(frame, (sx, sy), radius, color, -1)

    def _draw_object(self, frame, obj, mode):
        if mode == "3d":
            sx, sy, scale = self.project_3d(*obj.pos)
            r = max(5, int(obj.radius * scale))
        else:
            sx, sy = int(obj.pos[0]), int(obj.pos[1])
            r = obj.radius
            scale = 1.0

        # Sphere shading: brighter circle offset slightly for 3D feel
        cv2.circle(frame, (sx, sy), r, (60, 180, 255), -1)
        cv2.circle(frame, (sx - r//4, sy - r//4), r//3, (200, 230, 255), -1)
        cv2.circle(frame, (sx, sy), r, (30, 130, 200), 2)

        # Shadow on ground
        shadow_y = self.H - 10
        shadow_r = max(5, int(r * 0.6))
        cv2.ellipse(frame, (sx, shadow_y), (shadow_r, shadow_r//3),
                    0, 0, 360, (30, 30, 30), -1)

    def _draw_vectors(self, frame, obj, mode):
        if mode == "3d":
            sx, sy, scale = self.project_3d(*obj.pos)
        else:
            sx, sy = int(obj.pos[0]), int(obj.pos[1])
            scale = 1.0

        origin = (sx, sy)

        # Velocity vector (green)
        vel_scale = 0.15
        vx = int(sx + obj.vel[0] * vel_scale)
        vy = int(sy + obj.vel[1] * vel_scale)
        cv2.arrowedLine(frame, origin, (vx, vy), (0, 255, 0), 2, tipLength=0.3)

        # Acceleration / net force vector (red) -- shown as gravity direction
        ax = int(sx)
        ay = int(sy + 40)   # just shows gravity direction
        cv2.arrowedLine(frame, origin, (ax, ay), (0, 0, 255), 2, tipLength=0.3)

    def _draw_stats(self, frame, obj, mode):
        if mode == "3d":
            sx, sy, _ = self.project_3d(*obj.pos)
        else:
            sx, sy = int(obj.pos[0]), int(obj.pos[1])

        ke = obj.kinetic_energy()
        pe = obj.potential_energy(self.H, 500)
        speed = np.linalg.norm(obj.vel)

        text_x = sx + obj.radius + 5
        text_y = sy - 10
        cv2.putText(frame, f"v={speed:.0f}", (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        cv2.putText(frame, f"KE={ke:.0f}", (text_x, text_y+15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,100), 1)
        cv2.putText(frame, f"PE={pe:.0f}", (text_x, text_y+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100,100,255), 1)

    def draw_hud(self, frame, mode, paused, gesture):
        color = (0, 255, 0) if not paused else (0, 0, 255)
        cv2.putText(frame, f"Mode: {mode.upper()}  {'[PAUSED]' if paused else ''}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Gesture: {gesture}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

        # Legend
        legends = [
            ("Point = grab/throw", (0,255,0)),
            ("Pinch = spawn",      (255,200,0)),
            ("Fist = delete",      (0,100,255)),
            ("Palm = pause",       (200,200,200)),
            ("Peace = 2D/3D",      (255,100,255)),
        ]
        for i, (text, col) in enumerate(legends):
            cv2.putText(frame, text, (10, frame.shape[0] - 110 + i*22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, col, 1)