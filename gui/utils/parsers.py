
def conversion(options, key):
    """ Tries to return the value of a given key of given dict

    :returns None if keyerror, otherwise the value
    """
    try:
        return options[key].get()
    except KeyError:
        return None
