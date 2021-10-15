def proc_wrapper(func, *args, **kwargs):
    """Print exception because multiprocessing lib doesn't return them right."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(e)
        raise