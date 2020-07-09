

def describe_signal(signal, name="") :
    print("-------",name,"------")
    print(type(signal))
    print(len(signal))
    print(max(signal))
    print(min(signal))
    print("-------",name,"------")

def get_secs(t_string):
    '''
    from  time_string like '00:00:35.660' returns the 
    number of seconds respect to '00:00:00.000'
    return value is float
    '''

    hours = t_string[0:2]
    minutes = t_string[3:5]
    secs = t_string[6:8]
    m_secs = t_string[8:12]

    secs_total = int(hours)*3600 + int(minutes)*60 + int(secs) + float(m_secs)
    # print(hours,",", minutes,",", secs ,",", m_secs)
    # print (secs_total)
    return secs_total
