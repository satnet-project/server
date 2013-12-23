import logging
logger = logging.getLogger(__name__)
import re
p = re.compile('^op_([0-9]+)$')
p_id = re.compile('([0-9]+)')

def get_user_operations(request):
    """
    This function returns a dictionary with the set of operations (as values) 
    to be carried out over each user (as keys). Only a single operation is 
    permitted over a single user.
    
    :param request:
        The data input from the page's form
    :type request:
        Dictionary (Python Framework)
    :returns:
        A dictionary with the operations found
    :rtype:
        Dictionary (Python Framework)
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
        
    """

    operations = {}

    for i, j in request.iteritems():
        logger.debug(__name__ + '#### i = ' + i + ', j = ' + j)
    
    for k, operation in request.iteritems():
        
        if not p.match(k):
            continue
        
        ids = p_id.findall(k)

        if len(ids) != 1:
            continue
        
        user_id = ids.pop() 
        operations[user_id] = operation

    return operations

