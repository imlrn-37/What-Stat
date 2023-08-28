import re
import pandas as pd


def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2} - "

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # put the data into a dataframe

    df = pd.DataFrame({"user_message": messages, "message_date": dates})


    # convert the message_date type

    df["message_date"] = pd.to_datetime(df["message_date"], format='%m/%d/%y, %H:%M - ')

    # renaming the column

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate the name of users and their messages

    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split(r"^([^:]+): (.+)$", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group notifications")
            messages.append(entry[0])

    df['user'] = users
    df["message"] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df["date_only"]=df["date"].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))

    df["period"]=period



    return df

