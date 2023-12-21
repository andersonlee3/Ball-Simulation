import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# function that draws each frame of the animation
def animate(i):
    t = 0
    t_final = 50
    dt = 0.02
    red_location = np.array((0.75, 0.25))
    blue_location = np.array((0.25, 0.275))
    red_speed = np.array((-0.1, 0.5))
    blue_speed = np.array((0.11, 0.2))
    alpha = 0.8
    beta = 0.98

    while t < t_final:
        dt = 0.02
        temp_red = red_location + dt * red_speed #supposed new red location
        temp_blue = blue_location + dt * blue_speed #supposed new blue location
        red_wall = False #bool to check if red ball collided with wall
        blue_wall = False #bool to check if blue ball collided with wall
        col = False #bool to check if balls collided with each other

        #check if red ball went out of bounds
        if temp_red[1] >= 0.95 or temp_red[1] <= 0.05 or temp_red[0] >= 0.95 or temp_red[0] <= 0.05: 
            #calculate red location so that it just touches wall, the new dt, and the new speed
            temp_red_w, dt_red_w, red_speed_w = outOfBounds(temp_red, red_location, red_speed, alpha, beta)
            red_wall = True
        
        #check if blue ball went out of bounds
        if temp_blue[1] >= 0.95 or temp_blue[1] <= 0.05 or temp_blue[0] >= 0.95 or temp_blue[0] <= 0.05:
            #calculate blue location so that it just touches wall, the new dt, and the new speed
            temp_blue_w, dt_blue_w, blue_speed_w = outOfBounds(temp_blue, blue_location, blue_speed, alpha, beta)
            blue_wall = True

        #check if balls collide with each other
        if collision(temp_red, temp_blue):
            #calculate the locations so that the balls just touch each other, swap the speeds, and get new dt
            col = True
            temp_blue_c, temp_red_c, red_speed_c, blue_speed_c, dt_c = collisionCalc(red_location, blue_location, red_speed, blue_speed)

        #red and blue location equal new location if never collides with wall or each other
        red_location = temp_red
        blue_location = temp_blue

        #update correct locations speeds, and dts if balls collide with wall or each other
        if red_wall:
            red_location = temp_red_w
            red_speed = red_speed_w
            dt = dt_red_w
        if blue_wall:
            blue_location = temp_blue_w
            blue_speed = blue_speed_w
            dt = dt_blue_w
        if col:
            red_location = temp_red_c
            red_speed = red_speed_c
            blue_location = temp_blue_c
            blue_speed = blue_speed_c
            dt = dt_c

        x1_animation.append(red_location[0])
        y1_animation.append(red_location[1])
        x2_animation.append(blue_location[0])
        y2_animation.append(blue_location[1])
        #print(dt)
        #print(t)
        t += dt

    ax.clear()
    ax.set_aspect(1)
    circle1 = plt.Circle((x1_animation[i], y1_animation[i]), 0.05, color="red")
    circle2 = plt.Circle((x2_animation[i], y2_animation[i]), 0.05, color="blue")
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.set_facecolor("forestgreen")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

def outOfBounds(new_location, old_location, vel, alpha, beta):
    #right wall
    if new_location[0] >= 0.95:
        dt_new = abs((1 - old_location[0] - 0.05) / vel[0])
        new_location[0] = old_location[0] + dt_new * vel[0]
        new_location[1] = old_location[1] + dt_new * vel[1]
        vel[0] = -alpha * vel[0]
        vel[1] = beta * vel[1]
        return new_location, dt_new, vel
    #left wall
    elif new_location[0] <= 0.05:
        dt_new = abs((old_location[0] - 0.05) / vel[0])
        new_location[0] = old_location[0] + dt_new * vel[0]
        new_location[1] = old_location[1] + dt_new * vel[1]
        vel[0] = -alpha* vel[0]
        vel[1] = beta * vel[1]
        return new_location, dt_new, vel
    #bottom wall
    elif new_location[1] <= 0.05:
        dt_new = abs((old_location[1] - 0.05) / vel[1])
        new_location[0] = old_location[0] + dt_new * vel[0]
        new_location[1] = old_location[1] + dt_new * vel[1]
        vel[0] = beta * vel[0]
        vel[1] = -alpha * vel[1]
        return new_location, dt_new, vel
    #top wall
    elif new_location[1] >= 0.95:
        dt_new = abs((1 - (old_location[1] + 0.05)) / vel[1])
        new_location[0] = old_location[0] + dt_new * vel[0]
        new_location[1] = old_location[1] + dt_new * vel[1]
        vel[0] = beta * vel[0]
        vel[1] = -alpha * vel[1]
        return new_location, dt_new, vel


def collision(new_red_location, new_blue_location):
    #check for collisions
    rel_dist = math.sqrt(pow((new_red_location[0] - new_blue_location[0]), 2) + pow((new_red_location[1] - new_blue_location[1]), 2))
    #print(rel_dist)
    if rel_dist < 0.1:
        return True
    return False

def collisionCalc(old_red_location, old_blue_location, red_speed, blue_speed):
    #calulates location so that blue and red ball just touch and supposed velocities of each ball after they collide
    rel_dist = math.sqrt(pow(old_red_location[0] - old_blue_location[0], 2) + pow(old_red_location[1] - old_blue_location[1], 2))
    rel_speed = math.sqrt(pow(red_speed[0] - blue_speed[0], 2) + pow(red_speed[1] - blue_speed[1], 2))
    dt_new = abs((rel_dist - 0.1) / rel_speed)
    new_blue_location = old_blue_location + dt_new * blue_speed
    new_red_location = old_red_location + dt_new * red_speed
    x_direction = new_blue_location[0] - new_red_location[0]
    y_direction = new_blue_location[1] - new_red_location[1]
    length = math.sqrt(pow(new_blue_location[0] - new_red_location[0], 2) + pow(new_blue_location[1] - new_red_location[1], 2))
    normal = np.array([x_direction / length, y_direction / length])
    tangent = np.array([-normal[1], normal[0]])
    red_normal = np.dot(red_speed, normal)
    blue_normal = np.dot(blue_speed, normal)
    red_tangent = np.dot(red_speed, tangent)
    blue_tangent = np.dot(blue_speed, tangent)
    red_speed = blue_normal * normal + red_tangent * tangent
    blue_speed = red_normal * normal + blue_tangent * tangent
    return new_blue_location, new_red_location, red_speed, blue_speed, dt_new

# create empty lists for the x and y coordinates
x1_animation = []
y1_animation = []
x2_animation = []
y2_animation = []

# create the figure and axes objects
fig, ax = plt.subplots()

# run the animation
ani = FuncAnimation(fig, animate, frames=2500, interval=100, repeat=False)

plt.show()
