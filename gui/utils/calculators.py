
def center(parent, width=None, height=None):
    """ Creates the a string that is used to center a widget on the screen using geometry method

    :return string used in widget's geometry method
    """
    if not width:
        width = parent.winfo_width()
    if not height:
        height = parent.winfo_height()
    x = (parent.winfo_screenwidth() // 2) - (width // 2)
    y = (parent.winfo_screenheight() // 2) - (height // 2)
    return '{}x{}+{}+{}'.format(width, height, x, y)
