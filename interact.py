import bpython
import inspect
 
def interact():
    """
    Just run interace() anywhere in your code, and you'll get a sweet
    interactive bpython interpreter with access to the scope of where you
    called it. Great for investigating new API's.
    """
    try:
        stack = inspect.stack()
        scope = stack[1][0]
        vars = scope.f_globals.copy()
        vars.update(scope.f_locals)
    finally:
        del stack
    bpython.embed(locals_=vars)
