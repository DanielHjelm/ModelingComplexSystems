# Code is modified from https://github.com/alsignoriello/vicsek_model

import os, sys

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from math import pi, sqrt, cos, sin, atan2


#for videos
import moviepy.video.io.ImageSequenceClip

# ---------- Measurements ------------------- #
def calculatePolarisation(thetas, numberOfParticles):
    # Calculate cosine and sine sum
    cosSum = (np.sum(np.cos(thetas)))**2
    sinSum = (np.sum(np.sin(thetas)))**2
    # Polarisation
    polarisation = 1/numberOfParticles*np.sqrt(cosSum+ sinSum)

    return polarisation




#---------- Geometric functions -----------------------------

def vector_2_angle(v):
    x = v[0]
    y = v[1]
    return atan2(y,x)


# generate random angle theta between -pi - pi
def rand_angle():       
    theta = np.random.uniform(-pi,pi)
    return theta


# returns angle unit vector
def angle_2_vector(theta):
    x = cos(theta)
    y = sin(theta)
    
    # transform to unit vector
    v1 = np.array([x,y])
    #v2 = np.array([0,0])
    #uv = unit_vector(v1,v2)

    uv = v1/ euclidean_distance(v1[0], v1[1], 0, 0)

    return uv


# Euclidean distance between (x,y) coordinates
def euclidean_distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


# Euclidean distance between (x,y) coordinates on 1 x 1 torus
def torus_distance(x1, y1, x2, y2):
    x_diff = min(abs(x1 - x2), 1 - abs(x1 - x2))
    y_diff = min(abs(y1 - y2), 1 - abs(y1 - y2))
    return sqrt(x_diff**2 + y_diff**2)


def unit_vector(v1, v2):
    vector = v1 - v2
    dist = euclidean_distance(v1[0], v1[1], v2[0],v2[1])
    v1v2 = vector / dist
    return v1v2


#---------------------------------------------------------------------------------------

#-------------------------Functions of Neighbours --------------------------------------


# returns a list of indices for all neighbors
# includes itself as a neighor so it will be included in average
def get_neighbors(particles, r, x0, y0):

    neighbors = []

    for j,(x1,y1) in enumerate(particles):
        dist = torus_distance(x0, y0, x1, y1)

        if dist < r:
            neighbors.append(j)

    return neighbors


# average unit vectors for all angles
# return average angle by converting to vectors, using vector addition top-to-tail, then taking arc tan to get angle of resulting vector.
def get_average(thetas, neighbors):
    
    n_neighbors = len(neighbors)
    avg_vector = np.zeros(2)

    for index in neighbors:
        theta = thetas[index,0]
        theta_vec = angle_2_vector(theta)
        avg_vector += theta_vec

    avg_angle = vector_2_angle(avg_vector)

    return avg_angle


#-------------------------------------------------------------------------


def plot_vectors(coords, thetas):

	# generate random color for every particle
	colors = ["b", "g", "y", "m", "c", "pink", "purple", "seagreen",
			"salmon", "orange", "paleturquoise", "midnightblue",
			"crimson", "lavender"]

	
	for i, (x, y) in enumerate(coords):

		c = colors[i % len(colors)]

		# plot point
		plt.scatter(x, y, color = c, marker = ".")

		# plot tail
		theta = thetas[i]
		v = angle_2_vector(theta)
		x1 = x - (0.025 * v[0])
		y1 = y - (0.025 * v[1])
		plt.plot([x, x1], [y, y1], color=c)

	return



def save_plot(path, fname, eta):

    # axes between 0 and 1
    plt.axis([0, 1, 0, 1])

    # remove tick marks
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    # title 
    plt.title("η = %.2f" % eta)

    # save plot
    plt.savefig(os.path.join(path, fname[:-4]+".jpg"))
    plt.close()

    # clear for next plot
    plt.cla()

    return


# ------------------------------- RUNS FROM HERE -------------------------------

if __name__ == '__main__':
    polarisationList = []

    etas = np.linspace(0,1,50)
    numberOfSimulations = 50
    polarisationList = np.linspace(0, 1, numberOfSimulations*etas.size)
    for etaCount, eta in enumerate(etas):
        etaSim = eta       # noise in [0,1], add noise uniform in [-eta*pi, eta*pi]
        for sim in range(numberOfSimulations):
                    
            N = 40           # num of particles
            r = 0.5      # radius
            delta_t = 0.01   # time step

            # Maximum time
            t = 0.0
            T = 1 #was 2.0

            # Generate random particle coordinates
            # particles[i,0] = x
            # particles[i,1] = y
            particles = np.random.uniform(0, 1, size=(N, 2))

            # initialize random angles
            thetas = np.zeros((N, 1))
            for i, theta in enumerate(thetas):
                thetas[i, 0] = rand_angle()

            polarisation = 0

            # Currently run until time ends
            while t < T:

                for i, (x, y) in enumerate(particles):

                    # get neighbor indices for current particle
                    neighbors = get_neighbors(particles, r, x, y)

                    # get average theta angle
                    avg = get_average(thetas, neighbors)

                    # get noise angle
                    n_angle = rand_angle()

                    noise = etaSim * n_angle

                    # get new theta
                    thetas[i] = avg + noise

                    # move to new position 
                    particles[i,:] += delta_t * angle_2_vector(thetas[i])

                    # assure correct boundaries (xmax, ymax) = (1,1)
                    if particles[i, 0] < 0:
                        particles[i, 0] = 1 + particles[i, 0]

                    if particles[i, 0] > 1:
                        particles[i, 0] = particles[i, 0] - 1

                    if particles[i, 1] < 0:
                        particles[i, 1] = 1 + particles[i, 1]

                    if particles[i, 1] > 1:
                        particles[i, 1] = particles[i, 1] - 1

                # Calculate polarisation at last time step
                if round(t,2) == T-delta_t:
                    # Remove list within list to calculate polarization
                    calcThetas = [item for sublist in thetas for item in sublist]
                    # print(calcThetas)
                    polarisation = calculatePolarisation(calcThetas, len(particles))
                    print(f"Polarisation at simulation with eta {etaSim} and {sim} is: {polarisation}")
                    # new time step
                t += delta_t
            polarisationList[etaCount*numberOfSimulations+sim] = polarisation
            # print(polarisationList)

    etas = etas.repeat(numberOfSimulations)
    # plt.figure(1)
    # plt.scatter(etas, polarisationList)
    # plt.xlabel("\u03B7")
    # plt.ylabel(f"Number of sharers after {T} time steps")
    # plt.show()
    # Plotting
    plt.figure(2)
    plt.hist2d(etas, polarisationList, bins=10)
    plt.xlabel("\u03B7")
    plt.ylabel(f"Polarisation")
    plt.title("Phase transition plot of polarisation vs η")
    plt.colorbar()


plt.show()

    # print("Processing particles txt files to images", end='', flush=True)
    # txt_files = [i for i in os.listdir(particledir) if i.endswith(".txt")]
    # for fname in txt_files:
    #     print(end = ".", flush=True)
    #     f = os.path.join(particledir, fname) # the actual file

    #     # read in data
    #     mat = np.loadtxt(f)
    #     coords = mat[:,0:2]
    #     thetas = mat[:,2]
    #     plot_vectors(coords, thetas)
    #     save_plot(plotdir, fname, eta)
    # print()
    
    # # ------------- make the video ---------------
    # fps=3 #frames per second

    # jpg_files = sorted([i for i in os.listdir(plotdir) if i.endswith("jpg")])
    # jpg_files_paths = sorted([os.path.join(plotdir,i) for i in os.listdir(plotdir) if i.endswith("jpg")])

    # video_path = os.path.join(simdir, "spp.mp4")

    # clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(jpg_files_paths, fps=fps)
    # clip.write_videofile(video_path)