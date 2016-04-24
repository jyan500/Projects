# Submitter: yanjl(Yan, Jansen)
# Partner  : figuerp1(Figueroa, Pablo)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # set name to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        # Decode the annotation here and check it 
        def typeCheck():    
            assert isinstance(value, annot), '{} is the wrong type, should be type {}'.format(param, annot)
        def listcheck():
            # checks to see if value is a list or not
            assert isinstance(value, type(annot)), '{} is the wrong type, should be type {}'.format(param, type(annot))
            if len(annot) == 1:
                for vals in value:
                    self.check(param, annot[0], vals)
                    # recursively call self.check with progressively smaller annot (since annot may be a nested list/tuple)
                        
            if len(annot) > 1:
                assert len(annot) == len(value), 'length of annotation list must be the same as length of the argument'
                for item1, item2 in zip(annot, value):
                    assert isinstance(item2, item1)
                    
        def dictcheck():
            assert isinstance(value, type(annot)), '{} is the wrong type, should be type {}'.format(param, type(annot)) 
            assert len(annot.items()) == 1, 'annot can\'t have more than one key-value pair'
            check_type1 = list(annot.items())[0][0]
            check_type2 = list(annot.items())[0][1]
            if type(check_type1) is not Check_All_OK and type(check_type2) is not Check_Any_OK:
                for key, v in annot.items():
                        for key1, value1 in value.items():
                            assert isinstance(key1, key) and isinstance(value1, v), 'key and value must match corresponding annotations'
            else:
                for key, v in value.items():
                    # Check_All_OK establishes the condition necessary for key 
                    # Check_Any_OK establishes the  condition necessary for value
                    classCheck(check_type1, param, key) # compare the key to condition in Check_All_OK.__check_annotation__
                    classCheck(check_type2, param, v)   # compare the value to condition in Check_Any_OK.__check_annotation__
            
        def setcheck():
            assert isinstance(value, type(annot)), '{} is the wrong type, should be type {}'.format(param, type(annot)) 
            assert len(annot) == 1, 'length of annotation must be 1'
            for type_value in annot:
                for item in value:
                    assert isinstance(item, type_value), 'type inside annotation must be the same type as argument'
        def lambdacheck(): 
            assert len(annot.__code__.co_varnames) == 1
            try:
                assert annot(value), 'lambda must return true'
            except TypeError:
                raise AssertionError
        def classCheck(a, p, v):
            try:
                a.__check_annotation__(self.check, p, v, check_history)
            except AttributeError:
                raise AssertionError
          
        if type(annot) is type:
            typeCheck()
        elif type(annot) is list or type(annot) is tuple:
            listcheck()
        elif type(annot) is dict:
            dictcheck()
        elif type(annot) is set or type(annot) is frozenset:
            setcheck()
        elif inspect.isfunction(annot):   
            lambdacheck()
        else:
            if annot is not None:
               assert '__check_annotation__' in annot.__dict__, 'no method __check_annotation__'
        
                
                
                       
        
        
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        if Check_Annotation.checking_on == False or self.checking_on == False:
            return self._f(*param_arg_bindings())
        parameters = param_arg_bindings() 
        annotations = self._f.__annotations__
        #values = self._f(*parameters)
        
        
        try:
            # Check the annotation for every parameter (if there is one)
            for parameter, argument in parameters.items():
                if parameter in annotations:
                    self.check(parameter, annotations[parameter], argument)
                    
                    
                        
            # Compute/remember the value of the decorated function
            decorated_value = self._f(*parameters.values())
            # If 'return' is in the annotation, check it
            if 'return' in annotations:
                parameters['_return'] = decorated_value
                self.check('_return', self._f.__annotations__['return'], decorated_value)
            return decorated_value
            # Return the decorated answer
            
            #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
#             print(80*'-')
#             for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
#                 print(l.rstrip())
#             print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
#     def d(x:int,y,z:int) ->str: 
#         return str(x + y)
#     b = Check_Annotation(d)
#     b(3, 5, 9)
#     def stuff(x: None): pass
#     b1 = Check_Annotation(stuff)
#     b1(3)
#     def f(x:int): pass
#     f = Check_Annotation(f)
#     f(3)
#     def f(x : [[str]]): pass
#     f = Check_Annotation(f)
#     f([['a','b'],['c','d']])
    def f(x : {Check_All_OK(str,lambda x : len(x)<=3):Check_Any_OK(str,int)}): pass
    f = Check_Annotation(f)
    f({'a' : 1, 'b': 2, 'c':'c'})
    
#     def b(x : int) -> str:
#         return 0
#     d = Check_Annotation(b)
#     d(2)
           
    import driver
    driver.driver()
