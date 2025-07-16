# test funzioni
def testEqual(x, y):
    return x == y

# test eccezioni, passati se le eccezioni vengono lanciate correttamente
def testEccezione(n_test, eccezione, funzione, *args):
    """ Controlla che la funzione sollevi l'eccezione specificata
    """
    try:
        funzione(*args)
        print(f"Eccezione non sollevata nel test {n_test}")
        return False
    except eccezione:
        return True
    except Exception as e:
        print(f"Eccezione non attesa nel test {n_test}: ", repr(e))
        return False