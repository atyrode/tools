#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Callable, List, Tuple, Union

from termcolor import colored as alter
from termcolor import cprint

############################
#      Hello World!        #
############################

def meteovio_presents():
    
    @lambda _: _()
    class _:
        def __format__(_, __):
            _.__class__._ = property(lambda _: print(__))
            return ""

    def __() -> f"{_:Hello, world!}": ...

    _._

############################
#   Miscellaneous Var      #
############################

TERM_WIDTH = 80


############################
#    Func and elem manip   #
############################
#                          #
#   Reminder!              #
#   A decorator works      #
#   like this:             #
#                          #
#*   @decorator            #
#*    def foo():           #
#*        return True      #
#*                         #
#*  bar = decorator(foo()) #
#                          #
############################

def benchmark_annotation():
    
    """
        Goal of this benchmark:
        
            > Trying to hack: Function Annotation
            > https://peps.python.org/pep-3107/
    """
    
    #|========================================================================|#
    #|             Quick wrapper over print() to add a counter                |#
    #|          and a separator between each print. And is called             |#
    #|           using prt() for the focus to be on the annotation            |#
    
    step = 0
    def prt(*args, essay=0, **kwargs):
        nonlocal step
        
        #| Separator
        if essay:
            text = " " * len(f"[{step}]-> ") + f"= Essay {essay} ="
            args = alter(text, "green", attrs=["bold"]), *args
            
        #| Will add [x]-> before each print
        elif len(args) >= 1 and isinstance(args[0], int):
            step = args[0]
            args = alter(f"[{step}]->", "cyan", attrs=["bold"]), *args[1:]
            
        return __builtins__.print(*args, **kwargs)
    def f():pass
    _ = 0
    '''
    lambda: print(1, test.__annotations__)
    a = 10
    '''
    #|                                                                        |#
    #|========================================================================|#
    #|                 Hang on! Just need some wrapper here                   |#
    #|  
    #|  I'll be using this to print the annotation and the result of the lambda
    f;              getanno = lambda: test.__annotations__
    _;              anno = lambda func: func.__annotations__['return']
    _;              sanno = lambda f, *a, **k: anno(f)(*a, **k)

    ...;                 a = 10

    _=              anno = lambda func: func.__annotations__['return']
    _=              sanno = lambda f, *a, **k: anno(f)(*a, **k)
    
    
    print(anno, sanno, a)
    exit()
    #|               We got anno and set_anno! as a shortcut                  |#
    #|                                                                        |#
    #|                          Ok. Let's dive in.                            |#
    #==========================================================================#
    #|       In any given annoted method, I'm confident that I could          |#
    #|                                                                        |#
    #|            > Override the annotation part of a function.               |#
    #|            > Pass the args and kwargs of the function to it.           |#
    #|            > Call then lambda, and return the result.                  |#
    #|                                                                        |#
    #|            End goal is to bind all my thunks to a sort of              |#
    #|               "function factory" made out of this trick!               |#
    #|========================================================================|#
    prt(essay=1)
    
    #| Idea 1 - Default PEP
    def test(a, b) -> max(2, 9):        #< I wonder why the value is computed. Operands?
        return a + b
           
    prt(1, test.__annotations__)#*======> {'return': 9}
    prt(2, anno(test))#*================> 9
    
    #| Idea 2 - Variable testing
    def test()-> lambda n: max(0, n):
        return
    
    prt(3, anno(test))#*================> {'return': <function> at 0x7...>}
    lambda: prt(4, sanno(1))#*==========> Exception! (Int on __anno__)
    
    #| Idea 3 - Executing the lambda
    def test()-> lambda n: max(0, n)():
        return
    
    prt(5, anno(test))#*================> {'return': 0}
    
    #_____________________________________________________
    #######################################################
    #| Above was just a base test I found on PEP. Next we
    #| go from what I knew beforehand. We can declare
    #| the annotation as a lambda, so we can override it!
    #|
    #| From now on we'll always call our wrapper (anno)
    #| which binds to the return value of the annotation.
    prt(essay=2)
    
    def test() -> lambda n: n + 1:
        return
    
    print(getanno) # => {'return': <function at 0x7...>}
                # It only contains the lambda
             
    print(essay2())   # => None
    print(setanno(1))  # => 2
    print(setanno(2))  # => 3
    
    #_____________________________________________________
    ######################################################
    #| Here I'll try to extract the args from the function
    #| Then pass them to the lambda
    print(step=3)
    
    def test(*args, **kwargs) -> lambda n, *a, **k: n + 1:
        return # => Can't return arg 'n' of lambda, it's not defined
    
    print(test(1)) # => None. It does not evaluate the lambda and it shouldn't.
    
    func = test.__annotations__
    
    print(func) # => Exception, it's a dict with only the lambda
    
    #___________________________________________________
    ####################################################
    #| We need a different approach. One being a lambda
    #| decorator, or maybe inspect? Or some python
    #| base library that can do it for us.
    
    import inspect
    
    def test4(*args, **kwargs) -> lambda n, *a, **k: n + 1:
        return
    
    print(inspect.getfullargspec(test4)) # => FullArgSpec(args=[], varargs='args', varkw='kwargs', defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={'return': <function test4.<locals>.<lambda> at 0x7f...>})
    

# benchmark_annotation()
# # f = overrides the annotation part of the function
# g = lambda down: lambda *a, **k: print(down)
# f = lambda down: lambda *a, **k: down.__annotations__['return'](lambda: down(*a, **k))

# @lambda _: lambda: g(_)
# def h(*a, **k) -> function(): ...

# print( h(print) )

#==============================================================================#
"                                                                              "
"   __________                                                                 "
"   ALTER FUNC ---- thunks providing a way to manipulate functions and args    "
#==============================================================================#
# * tupnow()---> |  enforce the result args to be a tuple                      #
# * anon()-----> |  transforme the given func/args into anonymize counterpart  #
# * compute()--> |  executes an anonymized function wit the given args         #
# * wrap()-----> |  wraps a list of elements from a pattern                    #
# * churn()----> |  wraps a list of func/arg pair
#
class AlterFunc: #=============================================================#
    tupnow  = lambda args: args if isinstance(args, tuple) else (args,)        #
    anon    = lambda func: lambda *args, **kwargs: func(*args, **kwargs)       #
    compute = lambda func, args=(): af.anon(func)(af.tupnow(args))             #
    wrap    = lambda ele: [ele for ele in ele + ele[:-1][::-1]]                #
    churn   = lambda f_a_p: [af.compute(fu, ar) for fu, ar in af.wrap(f_a_p)]  #
#                                                                              #
af = AlterFunc() #=============================================================#
"                                                                              "
"   __________                                                                 "
"   ITER MANIP  -----  enhance your comment blocks; color strings; center;     "
#==============================================================================#
# * sbin()-------> |  ensure the number is either -1, 0 or 1                   #
# * favor()------> |  return a tuple of 2 binary values, 1 for the odd         #
# * maxlen()-----> |  return the smallest number between 2 numbers             #
# * center()-----> |  return the index center of a given list                  #
# * slice()------> |  return sliced list at index | odd ->offset->[left,right] #
# * halve()------> |  return havled                                            #
class StringManip: #===========================================================#
    sbin    = lambda nb: (nb > 0) - (nb < 0)                                   #
    favor   = lambda odd: (int(sm.sbin(odd) == -1), int(sm.sbin(odd) == 1))    #
    maxlen  = lambda el, le: min(el, le)                                       #
    center  = lambda el: len(el) // 2                                          #
    slice   = lambda el, idx, off: [el[:idx + off[0]], el[idx + 1 - off[1]:]]  #
    halve   = lambda el, odd=1: el if len(el) == 1 else sm.slice(el, sm.center(el), sm.favor(odd if len(el) % 2 else 1))
    flatten = lambda
    # Split a spliceable elemnts in the middle, with an optional odd option to decide which side to favor or if it should be removed
    def halve(self, el, odd=1) -> list: return el if len(el) == 1 else self.slice(el, self.center(el), self.vectorize(odd if len(el) % 2 else 1))
    
    # Flatten a list and its children until there is no more list
    def flatten(self, el) -> list: return el if not isinstance(el, list) else [item for sublist in el for item in self.flatten(sublist)]
    #
sm = StringManip() #===========================================================#


#==============================================================================#
""" PRETTIFY STR -- enhance your commentaries; color strings; center...      """
#==============================================================================#
# * bar()---->    creates a string of a given length with a char               #
# * mid()---->    creates a string with a centered text surrounded by a char   #
# * header()->    wraps a string into 2 bar and a mid                          #
class CommentGen: #============================================================#
    width  = 80                                                                #
    char   = "#"                                                               #
    bar    = lambda: cg.char * cg.width                                        #
    mid    = lambda text: af.wrap(cg.char, ' ', text.center(cg.width - 4, " "))#
    header = lambda text: "\n".join(af.churn( [(cg.bar, ()), (cg.mid, text)]) )#
cg = CommentGen() #============================================================#

class LogicManip:
    def __init__(self, width=80, char="#"):
        self.width = width
        self.char = char
    


    ########################
    # String manipulations #
    ########################
    

    
    ########################
    #   Prettify strings   #
    ########################
    
    def color(self, text, color="white"): pass
    def comment(self, text): pass
