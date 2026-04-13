import numpy as np
import matplotlib.pyplot as plt
import os

from data import *

# ---------------------------
# НАСТРОЙКИ
# ---------------------------
ANGLE_ERROR = 1
SAVE_DIR = "imgs"

os.makedirs(SAVE_DIR, exist_ok=True)


def experimental_error(I):
    """Экспериментальная погрешность"""
    return 0.05 * I + 1


def malus_theory(I0, angles):
    """Теоретическое значение"""
    return I0 * (np.cos(np.radians(angles)))**2


def malus_theory_error(I0, angles):
    """Погрешность теории"""
    alpha = np.radians(angles)
    dI = 2 * I0 * np.abs(np.cos(alpha) * np.sin(alpha))
    return dI * np.radians(ANGLE_ERROR)


def plot_with_errors(x, y, y_err, label, color=None):
    plt.errorbar(
        x, y,
        yerr=y_err,
        fmt='o',
        capsize=3,
        label=label,
        color=color
    )

def plot_theory_curve(I0, angle_min, angle_max, label):
    angles_dense = np.linspace(angle_min, angle_max, 500)
    theory_dense = malus_theory(I0, angles_dense)

    plt.plot(angles_dense, theory_dense, '-', label=label)


def fresnel_reflection(theta_deg, n=1.5):
    """Френель: возвращает R_perp и R_parallel"""
    theta = np.radians(theta_deg)

    sin_t = np.sin(theta) / n
    sin_t = np.clip(sin_t, -1, 1)
    theta_t = np.arcsin(sin_t)

    R_perp = (np.sin(theta - theta_t) / np.sin(theta + theta_t))**2
    R_parallel = (np.tan(theta - theta_t) / np.tan(theta + theta_t))**2

    return R_perp, R_parallel

def save_plot(name):
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/{name}.png", dpi=300)
    plt.close()


# ---------------------------
# 1. Закон Малюса
# ---------------------------
plt.figure()
plt.title("Закон Малюса")

angles = no_phase_degrees + 90

I0 = np.max(no_phase)
theory = malus_theory(I0, angles)

exp_err = experimental_error(no_phase)
theory_err = malus_theory_error(I0, angles)

plot_with_errors(angles, no_phase, exp_err, "Эксперимент")
plot_theory_curve(I0, angles.min(), angles.max(), "Теория")

plt.xlabel("Угол (градусы)")
plt.ylabel("Интенсивность")
plt.legend()
plt.ylim(0)
plt.grid()

save_plot("malus_law")


# ---------------------------
# 2. С пластинкой
# ---------------------------
"""plt.figure()
plt.title("С фазовой пластинкой")

angles = plast_degrees + 90

plot_with_errors(
    angles,
    plast,
    experimental_error(plast),
    "С пластинкой"
)

plot_with_errors(
    no_phase_degrees + 90,
    no_phase,
    experimental_error(no_phase),
    "Без пластинки"
)

plt.xlabel("Угол (градусы)")
plt.ylabel("Интенсивность")
plt.legend()
plt.grid()

save_plot("phase_plate")
"""

plt.figure()
plt.title("С фазовой пластинкой")

angles_no = no_phase_degrees
angles_plast = plast_degrees

# -------------------
# ЭКСПЕРИМЕНТ
# -------------------
plot_with_errors(
    angles_plast,
    plast,
    experimental_error(plast),
    "С пластинкой"
)

plot_with_errors(
    angles_no,
    no_phase,
    experimental_error(no_phase),
    "Без пластинки"
)

# -------------------
# ТЕОРИЯ
# -------------------

angles_dense = np.linspace(0, 180, 500)

I0 = np.max(no_phase)
phi0 = 90

theory_no = I0 * (np.cos(np.radians(angles_dense - phi0)))**2

plt.plot(
    angles_dense,
    theory_no,
    '--',
    label="Теория без пластинки"
)

# С пластинкой (обобщённая форма)
A = np.mean(plast)
B = (np.max(plast) - np.min(plast)) / 2
phi = 1 # фазовый сдвиг (можно подгонять)

theory_plast = A + B * np.cos(np.radians(2 * angles_dense + phi)) - 5

plt.plot(
    angles_dense,
    theory_plast,
    '--',
    label="Теория с пластинкой"
)

# -------------------
# ОФОРМЛЕНИЕ
# -------------------
plt.xlim(0)
plt.ylim(0)
plt.xlabel("Угол (градусы)")
plt.ylabel("Интенсивность")
plt.legend()
plt.grid()

save_plot("phase_plate")




# ---------------------------
# 3. Черное зеркало
# ---------------------------
plt.figure()
plt.title("Черное зеркало")

plot_with_errors(
    degreeses_step_10,
    dark_mirror,
    experimental_error(dark_mirror),
    "Эксперимент"
)

plt.xlabel("Угол")
plt.ylabel("Интенсивность")
plt.grid()

save_plot("dark_mirror")




# -------------------
# ТЕОРИЯ
# -------------------
angles_dense = np.linspace(15, 80, 500)

R_perp, R_parallel = fresnel_reflection(angles_dense)



scale = np.max(bruster_max)

plt.plot(
    angles_dense,
    R_perp * scale,
    '--',
    label="Горизонтальная (теория)"
)
plot_with_errors(
    brust_50_degreeses,
    bruster_min,
    experimental_error(bruster_min),
    "Эксперимент"
)

plot_with_errors(
    bruster_140_degrees,
    bruster_max,
    experimental_error(bruster_max),
    "Эксперимент"
)

plt.plot(
    angles_dense,
    R_parallel * scale,
    '--',
    label="Вертикальная (теория)"
)

# -------------------
# УГОЛ БРЮСТЕРА
# -------------------
min_idx = np.argmin(bruster_min)
brewster_angle = brust_50_degreeses[min_idx]

plt.axvline(
    brewster_angle,
    linestyle=':',
    label=f"θ_B ≈ {brewster_angle}°"
)

# -------------------
# ОФОРМЛЕНИЕ
# -------------------
plt.xlabel("Угол падения (градусы)")
plt.ylabel("Интенсивность")
plt.legend()
plt.grid()

save_plot("brewster_combined")