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

import pandas as pd
from IPython.core import display

def side_by_side(*objs, **kwds):
    space = kwds.get('space', 4)
    reprs = [repr(obj).split('\n') for obj in objs]
    print('-' * 40)
    print(pd.core.common.adjoin(space, *reprs))
    print('-' * 40)

def side_by_side2(*objs, **kwd):
    tables = [pd.DataFrame(df)._repr_html_() for df in objs]
    res = ""
    for t in tables:
        #style_pos = t.find('style="')+len('style="')
        #new_table = t[:style_pos] + "float:left;padding-right: 0.6em;" + t[style_pos:]
        TARGET = "<div"
        div_pos = t.find(TARGET) + len(TARGET)
        new_table = t[:div_pos] + ' style="float:left;padding-right: 0.6em;"' + t[div_pos:]
        res += new_table
    return res


