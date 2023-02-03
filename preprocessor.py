import pandas as pd
import re

def preprocess(data):
    datp1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    datp2 = '^(\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:d{1,2} \w\w)'
    pattern = datp1 or datp2
    #pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s' or '^(\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:d{1,2} \w\w)'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Converting Message Date Type...
    # dm= "%d/%m/%Y, %H:%M - "
    # md = "%m/%d/%Y, %H:%M - "
    # od = "%m/%d/%y, %H:%M - "
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    #df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - 'or' %m/%d/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # Separate users & Messages
    users = []
    messages = []
    for message in df['user_message']:

        entry = re.split('([\w\W]+?):\s', message)  # regex for name aur jbhtl : yeah nahi aata vpo regex hai
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
           # messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] =  df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['only_date'] = df['date'].dt.date

    return df


