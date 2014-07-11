"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

import logging
import re

logger = logging.getLogger('accounts')
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

