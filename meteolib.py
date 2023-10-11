#!/usr/bin/env python3

class LogicManip:
    def __init__(self, width=80, char="#"):
        self.width = width
        self.char = char
        self.text_params = {
            "colors": {
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "purple": "\033[35m",
                "cyan": "\033[36m",
                "lightgray": "\033[37m",
                "gray": "\033[90m",
                "reset": "\033[0m"
            },
            "styles": {
                "bold": "\033[1m",
                "underline": "\033[4m",
                "blink": "\033[5m",
                "reverse": "\033[7m",
                "concealed": "\033[8m"
            }
        }
        self.colors = self.text_params["colors"]
        self.styles = self.text_params["styles"]
        self.reset = self.colors["reset"]
    
    ########################
    # Func and elem manip  #
    ########################
    
    # Ensure tuple format for anonymous functions
    def forcetup(self, args) -> tuple: return args if isinstance(args, tuple) else (args,)
    
    # Transform a function into a lambda accepting any number of args
    def anonymize(self, func): return lambda *args, **kwargs: func(*args, **kwargs)

    # Compute execute an anonymized function with a given arg tuple
    def compute(self, func, args=()): return self.anonymize(func)(*args)
    
    # Wrap expands a list of elements from a pattern
    # Like: el1, el2, el3 ===== to ====== > el1, el2, el3, el2, el1
    def wrap(self, el) -> list: return [el for el in el + el[:-1][::-1]]
    
    # Churn wraps a list of func/arg pair, ensures args are tuples and computes the result
    def churn(self, func_arg_pairs) -> list: return [self.compute(func, self.forcetup(args)) for func, args in self.wrap(func_arg_pairs)]


    ########################
    #  Pretty comment gen  #
    ########################
    
    # Bar & Mid prints prettified separators
    def bar(self) -> str: return self.char * self.width
    
    def mid(self, text) -> str: return self.char + " " + text.center(self.width - 4, " ") + " " + self.char
    def pmid(self, text) -> None: (self.mid(text))

    # Header wraps a string into 2 bar and a mid
    def header(self, text="") -> str: return "\n".join( self.churn( [ (self.bar, ()) , (self.mid, text) ] ) )


    ########################
    # String manipulations #
    ########################
    
    # Ensures a number is either 1 or -1 or 0. False/True are converted to 0/1
    def sbin(self, nb) -> int: return (nb > 0) - (nb < 0)
    
    # This computes the offset to give to a slice to favor a side (0 = remove, -1 = left, 1 = right)
    def vectorize(self, odd) -> list: return int(self.sbin(odd) == -1), int(self.sbin(odd) == 1)
    
    # Sanitize an int to be no bigger than the provided list length
    def maxlen(self, el, le) -> int: return min(el, le)
    
    # Fetch index center of a given list
    def center(self, el) -> int: return len(el) // 2
    
    # Given a spliceable elemnts and an index, returns a list of the element sliced
    # Takes an offset [left, right] as binary values to favor a side, 0, 0 will discard
    # Uneven slicing
    def slice(self, el, index, offset) -> list: return [el[:index + offset[0]], el[index + 1 - offset[1]:]]
    
    # Split a spliceable elemnts in the middle, with an optional odd option to decide which side to favor or if it should be removed
    def halve(self, el, odd=1) -> list: return el if len(el) == 1 else self.slice(el, self.center(el), self.vectorize(odd if len(el) % 2 else 1))
    
    # Flatten a list and its children until there is no more list
    def flatten(self, el) -> list: return el if not isinstance(el, list) else [item for sublist in el for item in self.flatten(sublist)]
    
    ########################
    #   Prettify strings   #
    ########################
    
    def color(self, text, color="white"): pass
        