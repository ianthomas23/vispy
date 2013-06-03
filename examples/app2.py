""" More complete example for the app module.
This file also serves as a test for the behavior of the backends.
"""

import time
import random

import vispy
from vispy import app

app.use('qt')
# app.use('glut')
# app.use('pyglet')

# We'll use pyopengl for the drawing for now
import OpenGL.GL as gl
import OpenGL.GLU as glu


# todo: do we want key repeat or not?


class MyCanvas(app.Canvas):
    
    def __init__(self, *args, **kwargs):
        app.Canvas.__init__(self, *args, **kwargs)
        
        # Note that args args kwargs are used to initialize the native GUI window
        self.title = 'App demo'
        self.geometry = 50, 50, 300, 300
        
        self._color = 1, 0, 0
        self._mousepos = 0,0
        self.show()
    
    def on_initialize(self, event):
        print('initializing!')
    
    def on_close(self, event):
        print('closing!')
    
    def on_key_press(self, event):
        # Should repeat if held down
        modifiers = [key.name for key in event.modifiers]
        print('Key pressed - text: %r, key: %s, modifiers: %r' % (
                event.text, event.key.name, modifiers))
    
    def on_key_release(self, event):
        modifiers = [key.name for key in event.modifiers]
        print('Key released - text: %r, key: %s, modifiers: %r' % (
                event.text, event.key.name, modifiers))
    
    def on_mouse_move(self, event):
        # Should *always* fire (not only with mouse down)
        self.print_mouse_event(event, 'Mouse move')
    
    def on_mouse_press(self, event):
        # Should have right button
        # Should have right modifiers
        # Shpuld have right location
        self.print_mouse_event(event, 'Mouse press')
    
    def on_mouse_release(self, event):
        self.print_mouse_event(event, 'Mouse release')
    
    def on_mouse_wheel(self, event):
        # Should right have location
        self.print_mouse_event(event, 'Mouse wheel')
    
    def print_mouse_event(self, event, what):
        # Should print text when over the red square
        # Should always fire, not only when mouse pressed down
        if (    event.pos[0] < self.geometry[2]*0.5 
            and event.pos[1] < self.geometry[3]*0.5):
            
            modifiers = [key.name for key in event.modifiers]
            print('%s - pos: %r, button: %i, modifiers: %r, delta: %i' % (
                    what, event.pos, event.button, modifiers, event.delta))
    
    def on_resize(self, event):
        print('Resize %r' % (event.size, ))
    
    
    def on_paint(self, event):
        print('Drawing now (%f)' % time.time())
        
        # Set viewport and transformations
        gl.glViewport(0, 0, *self.geometry[2:])
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0.0, 1.0, 0.0, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Clear
        gl.glClearColor(1,1,1,1);
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        # Set color
        gl.glColor(*self._color)
        
        # Draw simple shape
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex(0.0,1.0); 
        gl.glVertex(0.0,0.5); 
        gl.glVertex(0.5,0.5); 
        gl.glVertex(0.5,1.0); 
        gl.glEnd()
        
        self._backend._vispy_swap_buffers()
    
    def change_color(self, event):
        self._color = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
        #self.update()  # Force redraw


if __name__ == '__main__':
    canvas = MyCanvas()
    
    # Setup a timer
    timer = app.Timer(1.0)
    timer.connect(canvas.change_color)
    timer.start()
    
    # Enter the mainloop
    app.run()
        