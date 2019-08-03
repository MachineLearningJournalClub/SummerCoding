# The MIT License (MIT)
# 
# Copyright (c) 2015 addfor s.r.l.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import bokeh.plotting as bk
from bokeh.models.ranges import Range1d

from . import palette as pal


def imagegrid(fig, images, grid_size=None, text=None,
              palette='Greys9', dw=1.0, dh=1.0, padding=0.2, border=0.2,
              quad_color='black',
              **kwargs):
    """Adds a grid of image glyphs to the given figure `fig'.

    Parameters:
      text (array-like) : text shown in the bottom-left corner of each image
      grid_size[0] (number) : number of images on each row of the grid
      grid_size[1] (number) : number of images on each column of the grid
      padding (number) : distance between each adjacent pair of images
      border (number) : amount of space left black around the grid
      quad_color (None or color) : 
          if not None, the color given the 1px border around each image
      **kwargs : 
          all other (keyword) arguments with name starting with "text_"
          will be passed, as they are, to the text glyphs.        

    Returns:
      rx, ry : 
           the width and height, respectively, of the total space taken
           up by the grid layout. 
    """
    
    if isinstance(palette, list):
        if isinstance(palette[0], tuple) and len(palette[0]) == 3:
            # Avoid a bug in Bokeh that renders only the blue channel
            palette = list(map(pal.to_hex, palette))

    if grid_size is None:
        grid_size = (len(images), 1)

    gw, gh = grid_size
    
    xs = np.array([ border + i*(dw + padding) for i in range(gw) ] * gh)
    ys = np.array([ border + j*(dh + padding) for j in range(gh) for i in range(gw) ])
        
    fig.image(image=images, x=xs, y=ys, palette=palette, dw=dw, dh=dh)
    if quad_color:
        fig.quad(left=xs, right=xs+dw, bottom=ys, top=ys+dh, 
                 line_color=quad_color, fill_color=None)
        
    if text:
        text_kwargs = dict(x=[ x+0.01 for x in xs ],
                           y=[ y-0.02 for y in ys ],
                           text=text, text_font_size='8pt')
        
        for k in list(kwargs.keys()):
            if not k.startswith("text_"):
                continue
            text_kwargs[k] = kwargs.pop(k)

        fig.text(**text_kwargs)

    rx = max(xs) + dw + border + (0.01 if quad_color else 0)
    ry = max(ys) + dh + border + (0.01 if quad_color else 0)

    return rx, ry


def imagegrid_figure(*args, **kwargs):
    """Creates a figure with a single image grid on it, created with imagegrid().
    This function exists mostly to make it easier to just get a simple image
    grid shown by Bokeh.
    The resulting Figure instance does not present any ticks on its
    axes, no grid, and no border on its outside.

    Parameters:
        All keyword parameters whose name starts with "figure_" is
        passed to the bokeh.plotting.figure() function after being
        stripped of the "figure_" prefix.

        All other arguments are passed to imagegrid. For this reason,
        you can refer to the documentation of `imagegrid' to know what
        other parameters are accepted by this function.

    Returns:
        A newly created `bokeh.plotting.Figure' instance.
    """
    
    figure_args = dict()

    for k in list(kwargs.keys()):
        if not k.startswith("figure_"):
            continue
        figure_args[k[7:]] = kwargs.pop(k)
        
    fig = bk.figure(**figure_args)
    rw, rh = imagegrid(fig, *args, **kwargs)
    fig.x_range = Range1d(0, rw)
    fig.y_range = Range1d(0, rh)
    
    fig.min_border = 0
    fig.grid.grid_line_color = None
    fig.axis.major_tick_out = 0
    fig.axis.major_tick_in = 0
    fig.axis.minor_tick_out = 0
    fig.axis.major_tick_out = 0
    fig.axis.axis_line_color = None
    fig.axis.major_label_text_color = None
    return fig


