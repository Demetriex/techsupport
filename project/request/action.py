def for_action(action):
    Repair_only = [
    'Computer Software Problem',
    'No Internet Connection',
    'Operating System Problem',
    ]
    if action in Repair_only:
        return 'repair_only'
    else:
        return None
