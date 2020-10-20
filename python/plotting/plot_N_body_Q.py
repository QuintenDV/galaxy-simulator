import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
from matplotlib import gridspec
import math
from matplotlib.colors import LinearSegmentedColormap
import matplotlib

import matplotlib.patches as patches
import matplotlib.path as path
from math import floor, log

from statistics import median # Voor de bewegende camera

""" READ DATA FROM FILE """

# files = ["resources/example_output.txt"]
files = ["resources/output.txt"]
filmpjes = ["filmpje_BCC.mp4"]
for filenumber in range(len(files)):

    # Read data from file
    data = []
    amount = 0 #Aantal deeltjes
    intro_frames = 20
    outro_frames = 100
    sim_frames = 1000
    number_of_frames =  sim_frames + intro_frames + outro_frames #Bij 0 plot hij alle frames

    OFFSET = [0, 0, 0]

    print("Read data")
    amount = 0
    data = []
    velocities = []
    energy = []
    stap_num = [] # Houdt bij de hoeveelste integratiestap het is (Enkel om te debuggen)
    with open(files[filenumber], "r") as ins:
        linenumber = 0
        trigger = -1 #die -1 doet niks doen ik -> remove?
        for line in ins:
            print(trigger)
            line_split = line.split(" ")
            if line_split[0] == "#": #Enkel voor eerste regel
                amount = int(line_split[1])
                num_steps = float(line_split[2])
                trigger = 1
                if sim_frames != 0:
                    trigger = int((num_steps*1.0)//((sim_frames)*1.0))
                    trigger = 1
                else:
                    sim_frames = int(num_steps)
                    number_of_frames = sim_frames + intro_frames + outro_frames
            else:			# Voor alle andere regels
                if linenumber % trigger == 0:
                    x = np.zeros(amount)
                    y = np.zeros(amount)
                    z = np.zeros(amount)
                    v = np.zeros(amount)
                    for i in range(0, amount):
                        x[i] = float(line_split[i * 4 + 1]) + OFFSET[0]
                        y[i] = float(line_split[i * 4 + 2]) + OFFSET[1]
                        z[i] = float(line_split[i * 4 + 3]) + OFFSET[2]
                        v[i] = float(line_split[i * 4 + 4])
                    data.append([x, y, z])
                    velocities.append(v)
                    energy.append(abs(float(line_split[-1]))/1000000000) # in c++ maal deze factor omdat hij geen te kleine waarden zou moeten wegschrijven
                    stap_num.append(int(float(line_split[0])))
                linenumber += 1

    data = data[:]
    print(len(data) == sim_frames, len(data), sim_frames)
    print("trigger ", trigger)
    """ Set up figure & 3D axis for animation """
    plot_color = '#101010'
    text_color = '#FFE8D5'
    plot_bg = "#3D3D3D"
    fig = plt.figure(facecolor = plot_color)
    gs = gridspec.GridSpec(2, 3)
    ax1 = fig.add_subplot(gs[:2,:2], projection='3d', facecolor=plot_color)
    ax2 = fig.add_subplot(gs[0,2], facecolor=plot_bg)
    ax3 = fig.add_subplot(gs[1,2], facecolor=plot_bg)
    ax3.set_aspect('auto')


    '''
    AX1: Showing particles
    '''

    # show axes
    ax1.plot([-100, 100],[0, 0], [0, 0], 'w-', lw = 0.3)
    ax1.plot([0,0], [-100, 100],[0, 0], 'w-', lw = 0.3)
    ax1.plot([0,0], [0, 0], [-100, 100], 'w-', lw = 0.3)

    #set right colors
    ax1.w_xaxis.set_pane_color((0.9, 0.9, 1, 0.0)) #Volledig doorzichtig
    ax1.w_yaxis.set_pane_color((0.9, 0.9, 1, 0.0))
    ax1.w_zaxis.set_pane_color((0.9, 0.9, 1, 0.0))

    #Assen uitschakelen
    ax1.set_axis_off()


    # set up lines and points
    marker_color = '#0060FF'
    pts = sum([ax1.plot([], [], [], 'o', markerfacecolor = marker_color, markeredgecolor = marker_color, markersize = 3)
               for _ in range(0, amount)], [])
    sc = ax1.scatter(data[:][0][0],data[:][1][0],data[:][2][0])

    # prepare the axes
    x_M = [0]*len(data)
    y_M = [0]*len(data)
    z_M = [0]*len(data)
    x_m = [0]*len(data)
    y_m = [0]*len(data)
    z_m = [0]*len(data)
    for j in range(len(data)):
        x_M[j] = (max(data[j][0]))
        y_M[j] = (max(data[j][1]))
        z_M[j] = (max(data[j][2]))
        x_m[j] = (min(data[j][0]))
        y_m[j] = (min(data[j][1]))
        z_m[j] = (min(data[j][2]))
    xM = max(x_M)
    xm = min(x_m)
    yM = max(y_M)
    ym = min(y_m)
    zM = max(z_M)
    zm = min(z_m)


    # Stel verschuiving in
    x_end = -2
    y_end = -2
    z_end = 0

    x_positions = np.linspace(0, x_end, sim_frames+1)
    x_positions = [x_positions[i]*math.sin(i/(len(x_positions))*math.pi/2)**3 for i in range(len(x_positions))]
    y_positions = np.linspace(0, y_end, sim_frames+1)
    y_positions = [y_positions[i]*((i/len(y_positions))**2)**3 for i in range(len(y_positions))]
    z_positions = np.linspace(0, z_end, sim_frames+1)
    z_positions = [z_positions[i]*((i/len(z_positions))**2) for i in range(len(z_positions))]

    ax1.axis("auto")
    view_width = 10
    end_view_width = 10
    ax1.set_xlim(-view_width, view_width)
    ax1.set_ylim(-view_width, view_width)
    ax1.set_zlim(-view_width, view_width)

    #view_widths = [end_view_width + 20*math.cos((i/(sim_frames-1))*math.pi/2)**5 for i in range(sim_frames+1)]


    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_zticklabels([])

    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    #ax1.view_init(30, 0)
    ax1.view_init(90, 0)

    # Set the time text
    frame_counter_label = ax1.text2D(0.05, 0.95, "Elapsed time: 0  (pause)", transform=ax1.transAxes, fontsize = 12, color = text_color)
    '''
    End Particles
    '''


    """
    AX2: Histogram
    """
    n, bins = np.histogram(velocities[0], 30)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n
    nrects = len(left)

    # here comes the tricky part -- we have to set up the vertex and path
    # codes arrays using moveto, lineto and closepoly

    # for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
    # CLOSEPOLY; the vert for the closepoly is ignored but we still need
    # it to keep the codes aligned with the vertices
    nverts = nrects*(1 + 3 + 1)
    verts = np.zeros((nverts, 2))
    codes = np.ones(nverts, int) * path.Path.LINETO
    codes[0::5] = path.Path.MOVETO
    codes[4::5] = path.Path.CLOSEPOLY
    verts[0::5, 0] = left
    verts[0::5, 1] = bottom
    verts[1::5, 0] = left
    verts[1::5, 1] = top
    verts[2::5, 0] = right
    verts[2::5, 1] = top
    verts[3::5, 0] = right
    verts[3::5, 1] = bottom

    barpath = path.Path(verts, codes)
    patch = patches.PathPatch(
    barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
    ax2.add_patch(patch)

    v_max = [max(V) for V in velocities]

    ax2.set_xlim(0, 1.5)
    ax2.set_ylim(bottom.min(), top.max())
    ax2.set_title("Velocity distribution", fontsize = 12, color=text_color)
    ax2.set_yticklabels([])
    ax2.tick_params(axis='x', colors=text_color, labelsize= 10)
    ax2.tick_params(axis='y', colors=text_color)
    xticks = ax2.xaxis.get_major_ticks()
    xticks[1].label1.set_visible(False)
    xticks[2].label1.set_visible(False)
    # xticks[4].label1.set_visible(False)
    # xticks[6].label1.set_visible(False)
    # xticks[8].label1.set_visible(False)



    '''
    End histogram
    '''

    '''
    Energy conservation
    '''

    h, = ax3.plot([], [], color = '#FF0E00')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(1e-7, max(energy))
    ax3.set_yscale('log')
    ax3.set_xlabel("Time", color = text_color)
    ax3.set_title("Energy conservation", fontsize = 12, color= text_color)
    ax3.set_xticklabels([])

    ax3.tick_params(axis='x', colors=text_color)
    ax3.tick_params(axis='y', colors=text_color)
    '''
    End energy conservation
    '''


    # initialization function: plot the background of each frame
    def init():
        xs = np.array(data[0][0][:], dtype=float)
        ys = np.array(data[0][1][:], dtype=float)
        zs = np.array(data[0][2][:], dtype=float)
        sc._offsets3d = (xs, ys, zs)
        return sc,

    # animation function.  This will be called sequentially with the frame number
    def animate(i, data):
        if (i < intro_frames):
            # intro
            print("intro ", i)

            azim = 60*(math.sin((i*math.pi/2)/intro_frames))**6
            #ax1.view_init(azim, 210*(math.cos((i*math.pi/2)/intro_frames)))

            outzoom = view_width*(0.05 + 0.95*math.sin((i*math.pi/2)/intro_frames)**6)
            ax1.set_xlim(- outzoom, outzoom)
            ax1.set_ylim(- outzoom, outzoom)
            ax1.set_zlim(- outzoom, outzoom)
            frame_counter_label.set_text("Elapsed time: " +"{0:.2f}".format(0) + "  (pause)")

        elif i > intro_frames + sim_frames:
            i -= (intro_frames + sim_frames)-1
            # outro
            print("outro ", i)

            azim = 60 - 90*math.sin((i/outro_frames)*math.pi/2)**6
            altazim = 90*(1 + 3*math.sin((i/outro_frames)*math.pi/2)**3)
            #ax1.view_init(azim, altazim)


            outzoom = end_view_width*(1 - 0.8*math.sin((i*math.pi/2)/outro_frames)**4)
            ax1.set_xlim(-outzoom + x_end, outzoom + x_end)
            ax1.set_ylim(-outzoom + y_end, outzoom + y_end)
            ax1.set_zlim(-outzoom + z_end, outzoom + z_end)
            frame_counter_label.set_text("Elapsed time: " +"{0:.2f}".format(stap_num[sim_frames]*0.0001) + "  (pause)")

        else:
            # simulatie
            i -= intro_frames
            print("simul ", i)
            ''' DEELTJES '''
            xs = np.array(data[i][0][:], dtype=float)
            ys = np.array(data[i][1][:], dtype=float)
            zs = np.array(data[i][2][:], dtype=float)
            sc._offsets3d = (xs, ys, zs)

            if i > (sim_frames)//2:
                azim = 60
            else:
                azim = 60#90*(2/3+ (1/3)*math.sin((i*math.pi)/(sim_frames)))
            #ax1.view_init(azim, 60 + 150 * (i / sim_frames))

            ax1.set_xlim(x_positions[i] - view_width, x_positions[i] + view_width)
            ax1.set_ylim(y_positions[i] - view_width, y_positions[i] + view_width)
            ax1.set_zlim(z_positions[i] - view_width, z_positions[i] + view_width)

            ''' HISTOGRAM '''
            to_bin = []
            for vel_i in range(len(velocities[i])):
                if velocities[i][vel_i] != 0:
                    to_bin.append(velocities[i][vel_i])
            n, bins = np.histogram(to_bin, 30)
            top = bottom + n
            verts[1::5, 1] = top
            verts[2::5, 1] = top


            ''' Enery conservation '''
            if i > 0:
                h.set_xdata(np.append(h.get_xdata(), i))
                h.set_ydata(np.append(h.get_ydata(), energy[i]))
                ax3.set_xlim(1, i+10)

            frame_counter_label.set_text("Elapsed time: " +"{0:.2f}".format(stap_num[i]*0.0001))
        fig.canvas.draw()
        # return tuple(pts) + (patch,) + (h, )
        return [sc] + [patch,] + [h, ]
    # instantiate the animator.
    print("Create animation")
    anim = animation.FuncAnimation(fig, animate, fargs=[data], init_func=init,
                                   frames=number_of_frames, interval=30, blit=True)

    # Save as mp4. This requires mplayer or ffmpeg to be installed
    print("Saving video...")
    # anim.save(filmpjes[filenumber], fps=22, extra_args=['-vcodec', 'libx264'], savefig_kwargs={'facecolor':plot_color}, dpi = fig.dpi * 8)
    print("Done")

    plt.show()
