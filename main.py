import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.ticker as mtick


fig = plt.figure(figsize=(9, 9))
ax = plt.gca()
ax.grid()
ln1, = ax.plot([], [], '-', color='k', lw=2)
ln2, = ax.plot([], [], '-', color='k', lw=2)
ln3, = ax.plot([], [], '-', color='k', lw=2)
ln4, = ax.plot([], [], '-', color='b', lw=2)
ln5, = ax.plot([], [], '-', color='r', lw=2)
ln6, = ax.plot([], [], '-', color='m', lw=2)
text_pt = plt.text(4, 5, '', color='b', fontsize=16)
text_pt1 = plt.text(4, 4.3, '', color='r', fontsize=16)
text_pt2 = plt.text(4, 3.6, '', color='m', fontsize=16)
theta = np.linspace(0, 2 * np.pi, 100)
r = np.linspace(0, 5, 100)
ry = np.linspace(0, 3, 100)
ra = np.linspace(0, 1, 100)
r_out = 5
r_out_x = 5
r_out_y = 3
e = 0.8
r_in = 0.05
E_0 = 0


def init():
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    x_out = [r_out * np.cos(theta[i]) for i in range(len(theta))]
    y_out = [r_out * np.sin(theta[i]) for i in range(len(theta))]
    x_track = [r_out_x * np.cos(theta[i]) for i in range(len(theta))]
    y_track = [r_out_y * np.sin(theta[i]) for i in range(len(theta))]
    ln1.set_data(x_out, y_out)
    ln3.set_data(x_track, y_track)
    return ln1, ln3


def run_animation():
    anim_running = True

    def onclick(event):
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    def update(i):
        global E_0
        x_in = [r_out * np.cos(theta[i]) + r_in * np.cos(theta[j]) for j in range(len(theta))]
        y_in = [r_out * np.sin(theta[i]) + r_in * np.sin(theta[j]) for j in range(len(theta))]
        x0 = [(np.sqrt((8*(np.cos(2*theta[i])))+17)) * ra[j] * np.cos(theta[i]) for j in range(len(theta))]
        y0 = [(np.sqrt((8*(np.cos(2*theta[i])))+17)) * ra[j] * np.sin(theta[i]) for j in range(len(theta))]
        print(x0, y0)
        M = [theta[i] / 2 / np.pi * 360 for i in range(len(theta))]
        E = M + e * np.sin(theta[i]) + e ** 2 * np.sin(theta[i]) * np.cos(theta[i]) + 0.5 * e**3 * np.sin(theta[i])*(3*np.cos(theta[i])*np.cos(theta[i])-1)
        ecos = [np.cos(E[i] / 180 * np.pi) for i in range(len(theta))]
        if E[i] <= 180:
            F = [np.arccos((ecos[i] - e) / (1 - e * ecos[i])) * 180 / np.pi for i in range(len(theta))]
        else:
            F = [-np.arccos((ecos[i] - e) / (1 - e * ecos[i])) * 180 / np.pi + 360 for i in range(len(theta))]
        x1 = [r[j] * np.cos(E[i] / 180 * np.pi) for j in range(len(theta))]
        y1 = [r[j] * np.sin(E[i] / 180 * np.pi) for j in range(len(theta))]
        x2 = [4 + (5 - 4 * np.cos(theta[i])) * ra[j] * np.cos(F[i] / 180 * np.pi) for j in range(len(theta))]
        y2 = [0 + (5 - 4 * np.cos(theta[i])) * ra[j] * np.sin(F[i] / 180 * np.pi) for j in range(len(theta))]
        text_pt.set_text("M=%.3f" % (M[i]))
        text_pt1.set_text("E=%.3f" % (E[i]))
        text_pt2.set_text("F=%.3f" % (F[i]))
        ln4.set_data(x0, y0)
        ln5.set_data(x1, y1)
        ln6.set_data(x2, y2)
        ln2.set_data(x_in, y_in)
        return ln2, ln4, ln5, ln6, text_pt, text_pt1, text_pt2,

    # ln1圆形 ln3椭圆 ln2卫星在圆轨道上轨迹 ln4平近点角M ln5偏近点角E ln6真近点角F

    fig.canvas.mpl_connect('button_press_event', onclick)
    anim = animation.FuncAnimation(fig, update, len(theta), init_func=init, interval=150)


run_animation()
plt.text(4, 0, '(4,0)', family='monospace', fontsize=12, color='y')
plt.text(0, 0, '(0,0)', family='monospace', fontsize=12, color='y')
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.show()
