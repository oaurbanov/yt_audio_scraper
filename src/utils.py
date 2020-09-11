import os


def describe_signal(signal, name=""):
    print("-------", name, "------")
    print("type: ", type(signal))
    print("len: ", len(signal))
    print("max: ", max(signal))
    print("min: ", min(signal))
    print("-------", name, "------")


def get_secs(t_string):
    """
    From  time_string like '00:00:35.660' returns the
    number of seconds respect to '00:00:00.000'
    returned value is float
    """

    hours = t_string[0:2]
    minutes = t_string[3:5]
    secs = t_string[6:8]
    m_secs = t_string[8:12]

    secs_total = int(hours) * 3600 + int(minutes) * 60 + int(secs) + float(m_secs)
    # print(hours,",", minutes,",", secs ,",", m_secs)
    # print (secs_total)
    return secs_total


def check_paths_exist(paths_array):
    for path in paths_array:
        if not os.path.lexists(path):
            print("Path does not exist: ", path)
            return False
    return True


def num_inside_limits(x, limits):
    """
    Evaluates if x is inside the limits(min, max)
    """
    if x >= limits[0] and x <= limits[1]:
        return True
    else:
        return False
