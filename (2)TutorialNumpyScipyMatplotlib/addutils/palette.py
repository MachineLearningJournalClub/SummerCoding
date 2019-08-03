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
"""
Color and color palette management helper functions.

This modules provides some simple functions to help with the management and
use of colors and color palettes. Although it was written to be used
with Bokeh, it doesn't really have any dependency, and can be used
anywhere else it could be useful.

Functions:
        linear_map - map (linearly) a sequence of real values to the given palette
        sample_mpl_cmap - convert a Matplotlib-like colormap to a simple array of colors
        to_rgb_bytes - converts a color expressed as an RGB [0.0, 1.0]-ranged tuple to a RGB bytes (int 0-255) tuple
        to_hex - converts a color expressed as an RGB [0.0, 1.0]-ranged tuple to a hex representation #aabbcc

Variables:
        mpl_cmap_jet - Colormap from Matplotlib: jet (deprecated)
        mpl_cmap_hot - Colormap from Matplotlib: hot

        jet_hex, hot_hex, jet_bytes, hot_bytes -
                *_hex: matplotlib colormap converted to hex representation
                *_bytes: matplotlib colormap converted to bytes (int 0-255) tuple
"""

mpl_cmap_jet = {'red': ((0., 0, 0), (0.35, 0, 0), (0.66, 1, 1), (0.89, 1, 1),
                        (1, 0.5, 0.5)),
                'green': ((0., 0, 0), (0.125, 0, 0), (0.375, 1, 1), (0.64, 1, 1),
                          (0.91, 0, 0), (1, 0, 0)),
                'blue': ((0., 0.5, 0.5), (0.11, 1, 1), (0.34, 1, 1),
                         (0.65, 0, 0), (1, 0, 0))}

mpl_cmap_hot = {'red':   ((0.       , 0.0416, 0.0416),
                          (0.365079 , 1.000000, 1.000000),
                          (1.0      , 1.0, 1.0)),
                'green': ((0.       , 0., 0.),
                          (0.365079 , 0.000000, 0.000000),
                          (0.746032 , 1.000000, 1.000000),
                          (1.0      , 1.0, 1.0)),
                'blue':  ((0.       , 0., 0.),
                          (0.746032 , 0.000000, 0.000000),
                          (1.0      , 1.0, 1.0))}

def sample(channel, pos):
    try:
        idx_b = next((idx for idx, it in enumerate(channel) if it[0] >= pos))
    except StopIteration:
        return channel[-1][1]

    idx_a = max(0, idx_b - 1)
    
    if idx_a == idx_b:
        return channel[idx_a][1]
        
    pos_a, val_a, _ = channel[idx_a]
    pos_b, val_b, _ = channel[idx_b]
    dx = (pos - pos_a) / (pos_b - pos_a)
    return val_a + dx * (val_b - val_a)

def sample_mpl_cmap(cmap, nsamples):
    channels = list(map(list, [ cmap['red'], cmap['green'], cmap['blue'] ]))
    for chan in channels:
        # Sort stops by position
        chan.sort(key=lambda stop: stop[0])

    positions = [ 1.0 / nsamples * i for i in range(nsamples+1) ]
    
    samples = []
    for pos in positions:
        r, g, b = [sample(chan, pos) for chan in channels]
        samples.append((r,g,b))
        
    return samples

jet = sample_mpl_cmap(mpl_cmap_jet, 80)
hot = sample_mpl_cmap(mpl_cmap_hot, 80)

def to_rgb_bytes(rgb):
    r, g, b = rgb[:3]
    r = int(min(1, r) * 255)
    g = int(min(1, g) * 255)
    b = int(min(1, b) * 255)
    return (r,g,b)

jet_rgb = list(map(to_rgb_bytes, jet))
hot_rgb = list(map(to_rgb_bytes, hot))

def to_hex(rgb):
    return "#%02x%02x%02x" % to_rgb_bytes(rgb)

jet_hex = list(map(to_hex, jet))
hot_hex = list(map(to_hex, hot))

def linear_map(xs, palette, low=None, high=None):
    """Map (linearly) a sequence of real values to the given palette.
    
    Parameters:
        xs - A list of numbers, in the range [low, high]
        palette - A list of colors

    Returns:
        A list of the same size of xs, with the color of each sample
    """
        
    if xs == []: return []
    
    if low == None:
        low = min(xs)
    if high == None:
        high = max(xs)

    idx = lambda x: int( (float(x) - low)
                         / (high - low)
                         * (len(palette)-1) )
    clamped = [ max(low, min(high, x)) for x in xs ]
    return [ palette[ idx(x) ] for x in clamped ]

