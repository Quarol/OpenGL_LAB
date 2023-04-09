    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(angle)
    axes()

    glColor3f(1.0, 1.0, 1.0)
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

            if i + 1 < N:
                glColor3f(colors[i+1][j][0], colors[i+1][j][1], colors[i+1][j][2])
                glVertex3f(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])

        glEnd()


    glFlush()