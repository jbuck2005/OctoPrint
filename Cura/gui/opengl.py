import math

from util import util3d
from util import profile

try:
	import OpenGL
	OpenGL.ERROR_CHECKING = False
	from OpenGL.GLU import *
	from OpenGL.GL import *
	hasOpenGLlibs = True
except:
	print "Failed to find PyOpenGL: http://pyopengl.sourceforge.net/"
	hasOpenGLlibs = False

def InitGL(window, view3D, zoom):
	# set viewing projection
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	size = window.GetSize()
	glViewport(0,0, size.GetWidth(), size.GetHeight())
	
	glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
	glLightfv(GL_LIGHT1, GL_POSITION, [1.0, 1.0, 1.0, 0.0])

	glEnable(GL_NORMALIZE)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_CULL_FACE)
	glDisable(GL_BLEND)

	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClearStencil(0)
	glClearDepth(1.0)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	aspect = float(size.GetWidth()) / float(size.GetHeight())
	if view3D:
		gluPerspective(45.0, aspect, 1.0, 1000.0)
	else:
		glOrtho(-aspect, aspect, -1, 1, -1000.0, 1000.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

def DrawMachine(machineSize):
	glColor3f(1,1,1)
	glLineWidth(4)
	glDisable(GL_LIGHTING)
	glBegin(GL_LINE_LOOP)
	glVertex3f(0, 0, 0)
	glVertex3f(machineSize.x, 0, 0)
	glVertex3f(machineSize.x, machineSize.y, 0)
	glVertex3f(0, machineSize.y, 0)
	glEnd()
	glLineWidth(2)
	glBegin(GL_LINES)
	for i in xrange(0, int(machineSize.x), 10):
		glVertex3f(i, 0, 0)
		glVertex3f(i, machineSize.y, 0)
	for i in xrange(0, int(machineSize.y), 10):
		glVertex3f(0, i, 0)
		glVertex3f(machineSize.x, i, 0)
	glEnd()
	glLineWidth(1)
	glBegin(GL_LINE_LOOP)
	glVertex3f(0, 0, machineSize.z)
	glVertex3f(machineSize.x, 0, machineSize.z)
	glVertex3f(machineSize.x, machineSize.y, machineSize.z)
	glVertex3f(0, machineSize.y, machineSize.z)
	glEnd()
	glBegin(GL_LINES)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 0, machineSize.z)
	glVertex3f(machineSize.x, 0, 0)
	glVertex3f(machineSize.x, 0, machineSize.z)
	glVertex3f(machineSize.x, machineSize.y, 0)
	glVertex3f(machineSize.x, machineSize.y, machineSize.z)
	glVertex3f(0, machineSize.y, 0)
	glVertex3f(0, machineSize.y, machineSize.z)
	glEnd()

	glPushMatrix()
	glTranslate(-5,-5,0)
	glLineWidth(2)
	glColor3f(0.5,0,0)
	glBegin(GL_LINES)
	glVertex3f(0,0,0)
	glVertex3f(20,0,0)
	glEnd()
	glColor3f(0,0.5,0)
	glBegin(GL_LINES)
	glVertex3f(0,0,0)
	glVertex3f(0,20,0)
	glEnd()
	glColor3f(0,0,0.5)
	glBegin(GL_LINES)
	glVertex3f(0,0,0)
	glVertex3f(0,0,20)
	glEnd()

	glDisable(GL_DEPTH_TEST)
	#X
	glColor3f(1,0,0)
	glPushMatrix()
	glTranslate(23,0,0)
	noZ = ResetMatrixRotationAndScale()
	glBegin(GL_LINES)
	glVertex3f(-0.8,1,0)
	glVertex3f(0.8,-1,0)
	glVertex3f(0.8,1,0)
	glVertex3f(-0.8,-1,0)
	glEnd()
	glPopMatrix()

	#Y
	glColor3f(0,1,0)
	glPushMatrix()
	glTranslate(0,23,0)
	ResetMatrixRotationAndScale()
	glBegin(GL_LINES)
	glVertex3f(-0.8, 1,0)
	glVertex3f( 0.0, 0,0)
	glVertex3f( 0.8, 1,0)
	glVertex3f(-0.8,-1,0)
	glEnd()
	glPopMatrix()

	#Z
	if not noZ:
		glColor3f(0,0,1)
		glPushMatrix()
		glTranslate(0,0,23)
		ResetMatrixRotationAndScale()
		glBegin(GL_LINES)
		glVertex3f(-0.8, 1,0)
		glVertex3f( 0.8, 1,0)
		glVertex3f( 0.8, 1,0)
		glVertex3f(-0.8,-1,0)
		glVertex3f(-0.8,-1,0)
		glVertex3f( 0.8,-1,0)
		glEnd()
		glPopMatrix()

	glPopMatrix()
	glEnable(GL_DEPTH_TEST)
	
def ResetMatrixRotationAndScale():
	matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
	noZ = False
	if matrix[3][2] > 0:
		return False
	scale2D = matrix[0][0]
	matrix[0][0] = 1.0
	matrix[1][0] = 0.0
	matrix[2][0] = 0.0
	matrix[0][1] = 0.0
	matrix[1][1] = 1.0
	matrix[2][1] = 0.0
	matrix[0][2] = 0.0
	matrix[1][2] = 0.0
	matrix[2][2] = 1.0
	
	if matrix[3][2] != 0.0:
		matrix[3][0] /= -matrix[3][2] / 100
		matrix[3][1] /= -matrix[3][2] / 100
		matrix[3][2] = -100
	else:
		matrix[0][0] = scale2D
		matrix[1][1] = scale2D
		matrix[2][2] = scale2D
		matrix[3][2] = -100
		noZ = True
	
	glLoadMatrixf(matrix)
	return noZ

def DrawBox(vMin, vMax):
	glBegin(GL_LINE_LOOP)
	glVertex3f(vMin.x, vMin.y, vMin.z)
	glVertex3f(vMax.x, vMin.y, vMin.z)
	glVertex3f(vMax.x, vMax.y, vMin.z)
	glVertex3f(vMin.x, vMax.y, vMin.z)
	glEnd()

	glBegin(GL_LINE_LOOP)
	glVertex3f(vMin.x, vMin.y, vMax.z)
	glVertex3f(vMax.x, vMin.y, vMax.z)
	glVertex3f(vMax.x, vMax.y, vMax.z)
	glVertex3f(vMin.x, vMax.y, vMax.z)
	glEnd()
	glBegin(GL_LINES)
	glVertex3f(vMin.x, vMin.y, vMin.z)
	glVertex3f(vMin.x, vMin.y, vMax.z)
	glVertex3f(vMax.x, vMin.y, vMin.z)
	glVertex3f(vMax.x, vMin.y, vMax.z)
	glVertex3f(vMax.x, vMax.y, vMin.z)
	glVertex3f(vMax.x, vMax.y, vMax.z)
	glVertex3f(vMin.x, vMax.y, vMin.z)
	glVertex3f(vMin.x, vMax.y, vMax.z)
	glEnd()

def DrawSTL(mesh):
	glEnable(GL_CULL_FACE)
	for face in mesh.faces:
		glBegin(GL_TRIANGLES)
		v1 = face.v[0]
		v2 = face.v[1]
		v3 = face.v[2]
		glNormal3f(face.normal.x, face.normal.y, face.normal.z)
		glVertex3f(v1.x, v1.y, v1.z)
		glVertex3f(v2.x, v2.y, v2.z)
		glVertex3f(v3.x, v3.y, v3.z)
		glNormal3f(-face.normal.x, -face.normal.y, -face.normal.z)
		glVertex3f(v1.x, v1.y, v1.z)
		glVertex3f(v3.x, v3.y, v3.z)
		glVertex3f(v2.x, v2.y, v2.z)
		glEnd()

def DrawGCodeLayer(layer):
	filamentRadius = profile.getProfileSettingFloat('filament_diameter') / 2
	filamentArea = math.pi * filamentRadius * filamentRadius
	lineWidth = profile.getProfileSettingFloat('nozzle_size') / 2 / 10
	
	fillCycle = 0
	fillColorCycle = [[0.5,0.5,0.0],[0.0,0.5,0.5],[0.5,0.0,0.5]]
	
	glDisable(GL_CULL_FACE)
	for path in layer:
		if path.type == 'move':
			glColor3f(0,0,1)
		if path.type == 'extrude':
			if path.pathType == 'FILL':
				glColor3fv(fillColorCycle[fillCycle])
				fillCycle = (fillCycle + 1) % len(fillColorCycle)
			elif path.pathType == 'WALL-INNER':
				glColor3fv([0,1,0])
			elif path.pathType == 'SUPPORT':
				glColor3fv([0,1,1])
			elif path.pathType == 'SKIRT':
				glColor3fv([0,0.5,0.5])
			else:
				glColor3fv([1,0,0])
		if path.type == 'retract':
			glColor3fv([0,1,1])
		if path.type == 'extrude':
			drawLength = 0.0
			prevNormal = None
			for i in xrange(0, len(path.list)-1):
				v0 = path.list[i]
				v1 = path.list[i+1]

				# Calculate line width from ePerDistance (needs layer thickness and filament diameter)
				dist = (v0 - v1).vsize()
				if dist > 0 and path.layerThickness > 0:
					extrusionMMperDist = (v1.e - v0.e) / dist
					lineWidth = extrusionMMperDist * filamentArea / path.layerThickness / 2

				drawLength += (v0 - v1).vsize()
				normal = (v0 - v1).cross(util3d.Vector3(0,0,1))
				normal.normalize()

				vv2 = v0 + normal * lineWidth
				vv3 = v1 + normal * lineWidth
				vv0 = v0 - normal * lineWidth
				vv1 = v1 - normal * lineWidth

				glBegin(GL_QUADS)
				glVertex3f(vv0.x, vv0.y, vv0.z - 0.01)
				glVertex3f(vv1.x, vv1.y, vv1.z - 0.01)
				glVertex3f(vv3.x, vv3.y, vv3.z - 0.01)
				glVertex3f(vv2.x, vv2.y, vv2.z - 0.01)
				glEnd()
				if prevNormal != None:
					n = (normal + prevNormal)
					n.normalize()
					vv4 = v0 + n * lineWidth
					vv5 = v0 - n * lineWidth
					glBegin(GL_QUADS)
					glVertex3f(vv2.x, vv2.y, vv2.z)
					glVertex3f(vv4.x, vv4.y, vv4.z)
					glVertex3f(prevVv3.x, prevVv3.y, prevVv3.z)
					glVertex3f(v0.x, v0.y, v0.z)
					
					glVertex3f(vv0.x, vv0.y, vv0.z)
					glVertex3f(vv5.x, vv5.y, vv5.z)
					glVertex3f(prevVv1.x, prevVv1.y, prevVv1.z)
					glVertex3f(v0.x, v0.y, v0.z)
					glEnd()
					
				prevNormal = normal
				prevVv1 = vv1
				prevVv3 = vv3
		else:
			glBegin(GL_LINE_STRIP)
			for v in path.list:
				glVertex3f(v.x, v.y, v.z)
			glEnd()
	glEnable(GL_CULL_FACE)
