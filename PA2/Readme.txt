Hanyang University CSE4020 Computer Graphics class by prof.Taesoo Kwon

Project Assignment 02
2021059507 김나은

1. Project Overview

-   This project animates a cow object along the Catmull-Rom spline curve defined by six control points.
    These control points are selected by Users.
-   The goal of this project is to make cow make smooth transitions between points.

2. Environment and Installation

-   MacBook Air M1 16GB RAM
-   python 3.11.5
-   PyOpenGL installed

3. Core Functions and Main Changes

    a. spline(t, p0, p1, p2, p3)
        - This function calculates Catmull-Rom spline positions. The formula is as follows.
            t2 = t * t
            t3 = t2 * t

            # Catmull-Rom spline
            0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)

        - This function determines the cow's position along the curve.
        
    b. cowFace(currentPos, nextPos)
        - This function adjusts cow's orientation to face the direction it is moving, along the spline curve.
        - This process is done through following steps
            i. calculates direction vector
            ii. computes rotation matrix
            iii. applies rotation matrix

    c. display()
        - Core function of this program, because this function contains rendering loop.
        - This function draws elements, and performs animation.
        - Functionalities are as follows
            i. sets viewing transformation and draws static elements (given as a skeleton code)
            ii. handles animation depending on 'animating' flag variable. if 'animating' is True,
                this function calculates cow's position and orientation along the catmull-rom spline curve,
                and draw the cow at the new position
            iii. if 'animating' is False, this function draws the cow at the selected control points
    
    d. onMouseButton(window, button, state, mods)
        - This function handles mouse button events.
        - This function enables selection of control points, and starts animation when 6 control points are selected

    e. onMouseDrag(window, x, y)
        - This function handles mouse drag events to update the cow's position.
        - This function supports both vertical and horizontal dragging.

4. Trouble Shooting

-   Had hardships making the cow see upside when moving upward. (Could not make it eventually)