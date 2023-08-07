def preprocess(data):
    import re
    import pandas as pd
    pattern = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s(?:am|pm) - '
    messages = re.split(pattern, data)[2:]
    dates = re.findall(pattern, data)[1:]
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for mess in df['user_message']:
        entry = re.split(r'^(.*?):\s*(.*)$', mess)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df
