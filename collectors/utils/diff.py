
#TODO: lists

def ldiff(l1, l2):
    '''List difference.

    '''
    
    # Get items
    s1 = set(l1)
    s2 = set(l2)
    s = s1 & s2

    # Get ordered disjunction
    return [i for i in l1 + l2 if i not in s]

def ddiff(d1, d2):
    '''Dictionary difference.

    '''
    
    # Initialize diff
    dd = {}
    
    # Loop over keys
    for k in (set(d1) | set(d2)):

        # Get values
        v1 = d1[k]
        v2 = d2[k]
        
        # Key only in one dict
        if k in d1 and not k in d2:
            dd[k] = v1
        elif k in d2 and not k in d1:
            dd[k] = v2

        # Value conflict
        elif v1 != v2:

            # Compare two dicts
            if isinstance(v1, dict) and \
                    isinstance(v2, dict):
                dd[k] = ddiff(v1, v2)
             
            # Compare two lists
            elif isinstance(v1, list) and \
                    isinstance(v2, list):
                dd[k] = ldiff(v1, v2)

            # Compare two values
            else:
                dd[k] = [v1, v2]
    
    # Done
    return dd
