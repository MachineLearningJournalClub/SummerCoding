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
"""IPython utility: automatic table of contents generation

Functions:
        js - get the JavaScript script that generates the TOC of the document
"""


JS_SCRIPT = """
$(function() {
    function regenTOC(){
        element = $("#toc-container");

	var toc = document.createElement("div");
	$(toc).attr("class", "table-of-contents");

	var curLevel = 0;
	var containerStack = [toc];
	var levelOfTag = {"h2": 1, "h3": 2, "h4": 3, "h5": 4};

	function pushLevel() {
            var list = document.createElement("ul");
            containerStack.push(list);
            curLevel++;
	}
	
	function popLevel() {
            var lastContainer = containerStack.pop();
            $(lastContainer).appendTo(containerStack[containerStack.length - 1]);
            curLevel--;
	}
	
	$(".text_cell_render :header").each(function (i, elem) {
            var level = levelOfTag[ elem.tagName.toLowerCase() ];

            if (level === undefined)
		return;

            while (curLevel < level)
		pushLevel();
            while (curLevel > level)
		popLevel();
            
            var listItem = document.createElement("li");
            var link = document.createElement("a");
            $(link)
		.text($(elem).contents().first().text()) // Remove the pilcrow sign
		.attr("href", "#" + $(elem).attr("id"))
		.appendTo(listItem);
            $(listItem).appendTo(containerStack[containerStack.length - 1]);
	});
	
	while (curLevel > 0)
            popLevel();

        $("<a class='btn-update' href='#'>Update</a>")
          .click(regenTOC).prependTo(toc);

	$(toc).prepend("<div class='title'>Contents</div>")
          .wrap("<div class='toc-headings'/>");

        $(element).empty();
        $(element).append(toc);
    }

    if (typeof(IPython) !== 'undefined')
        $([IPython.events]).on('notebook_loaded.Notebook', regenTOC);
    regenTOC();
});

"""

def js(ipy_notebook=False):
    """Get the JavaScript script that generates the TOC of the document.
    The returned script uses JQuery to access the DOM, and looks at
    the heading tags (i.e. <h1>, <h2>, ...) to create a table of
    contents.  The resulting table of contents is appended to the
    element #toc-container (which, in the case of an IPython notebook,
    is created in the output area of the cell).

    Parameters:
        ipy_notebook (bool) :
                When true, the script is returned wrapped in a
                IPython.display.HTML object. This makes it work
                automatically in any IPython notebook.

    Returns:
        (str or IPython.display.HTML) - The JS script

    The structure of the output is (if you want to style it with CSS, for example):
        div#table-of-contents div.title ("Contents")
                .toc-container
                        ul First
                                li First.1
                                li First.2
                                li First.3
                                ...
                        ul Second
                                li Second.1
                                li Second.2
                                        ul Second.2.1
                                                li Second.2.1.1
                                                li Second.2.1.2
                                                ...
                                        ...
                                ...
                        ...

    """
    if ipy_notebook:
        from IPython.display import HTML
        return HTML(data=("<div id='toc-container'>"
                          + "<script type='text/javascript'>"
                          + JS_SCRIPT
                          + "</script>"
                          +"</div>"))
    else:
        return JS_SCRIPT
