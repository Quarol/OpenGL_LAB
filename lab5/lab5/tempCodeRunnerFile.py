global theta, phi
    global light_position, light_position1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * movement_speed
        phi += delta_y * pix2angle * movement_speed

        theta %= 360
        phi %= 360 

        calc_light_position(light_position, 5, phi, theta, GL_LIGHT0)
        calc_light_position(light_position1, 5, phi + math.pi, theta, GL_LIGHT1)


    draw_light_source(light_position1)
    draw_light_source(light_position)