def country_from_icon(icon):
    c = icon[1].lower()
    if c in ['h', 's']: return 'ru'
    elif c in ['f', 'a']: return 'ua'
    else:
        print("Could not detect country: %s - %s" % (icon, c))
        return 'na'