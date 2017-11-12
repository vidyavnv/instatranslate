def cleanup():
    import sys
    import os
    from os import listdir

    directory = os.path.dirname(os.path.realpath(__file__))

    test = os.listdir( directory )

    for item in test:
        if not item.endswith(".py"):
            os.remove( os.path.join( directory, item ) )
