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

# my_module.py =========================================================
''' This is the documentation
      for my example module'''

'''Naming convenctions:
    Function names must be lowercase separated by underscores '_'
    An underscore '_' at the beginning of a functuin name means the function is
    intended to be private BUT Python do NOT enforce this rule:
    you can break the code if you want! '''

# Variables defined here are available for ALL the functions in the module
# When module is imported, these variable can be accessed with:
#    module_name.variable_name
module_variable = 1

# Constants are named in uppercase
MODULE_CONSTANT = 1

def my_function(name):
    ''' This is the documentation for "my_function"'''
    # Variables defined inside functions are local
    (first, family) = name                       # Arguments bundled in a Tuple
    return _my_private_function(first, family)

def _my_private_function(first_name, second_name):
    ''' This is the documentation for "_my_private_function"'''
    full_name = first_name + ' [' + second_name.upper() + ']'
    return full_name
    
if __name__ == '__main__':
    ''' This is a Unit Test: use "run my_module" from Python interpreter'''
    print('This is the testing code:')
    print(my_function(('Johnn', 'Doe')))
