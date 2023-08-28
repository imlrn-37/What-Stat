from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
import calendar
import numpy as np



extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user == "Overall":
        # fetch no of messages

        num_messages = df.shape[0]

        # fetch no of words
        words = []
        for message in df['message']:
            words.extend(message.split())

        # fetch the no of media messages
        num_media_msg = df[df['message'] == '<Media omitted>'].shape[0]

        # fetch the no of links

        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_msg, len(links)
    else:

        new_df = df[df["user"] == selected_user]
        # no of messages

        num_messages = new_df.shape[0]

        # no of words of a user

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        # fetch the no of media messages
        num_media_msg = new_df[new_df['message'] == '<Media omitted>'].shape[0]

        # fetch the no of links
        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_msg, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open("stopwords.txt", "r")
    stop_words = f.read().split()

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df['user'] != 'group notifications']
    temp = temp[temp['message'] != "<Media omitted>"]

    words = []

    for msg in temp["message"]:
        sentences = msg.split(".")  # Split the message into sentences
        for sentence in sentences:
            words_in_sentence = sentence.lower().split()  # Split sentence into words
            for word in words_in_sentence:
                if word not in stop_words:
                    words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_counter=Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counter.most_common(len(emoji_counter)))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+ str(timeline["year"][i]))

    timeline["time"]=time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    daily_timeline=df.groupby(["date_only"]).count()["message"].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    users_heatmap=df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    return users_heatmap

def sorted_timeline_desc(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    daily_times=df.groupby(["date_only"]).count()["message"].reset_index()

    sorted_daily_timeline= daily_times.sort_values(by='message', ascending=False)

    return sorted_daily_timeline.head(10)

def highest_years(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    year_counts= df['year'].value_counts().sort_index()

    return year_counts.head(4)

def msgs_per_hour(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # msgs per hour

    messages_per_hour = df['hour'].value_counts()

    # Calculate the total number of messages
    total_messages = messages_per_hour.sum()

    # Calculate the percentage of messages per hour
    percentage_per_hour = (messages_per_hour / total_messages) * 100

    average_percentage = percentage_per_hour.mean()

    average_percentage_formatted = round(average_percentage, 2)

    # avg no of words per message

    num_messages = df.shape[0]

    # fetch no of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    avg_words=len(words)/num_messages

    avg_words_formatted=round(avg_words,2)

    # average length of a message

    average_message_length = df['message'].apply(len).mean()

    average_message_length_formatted=round(average_message_length,2)



    return average_percentage_formatted, avg_words_formatted, average_message_length_formatted


def calender_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    years = df['year'].unique()

    heatmap_data = {}

    for year in years:
        year_data = df[df['year'] == year]
        month_day_matrix = np.zeros((7, 12))  # Matrix to store counts for each day of week and month

        for _, row in year_data.iterrows():
            month = row["month_num"] - 1 # Adjust month index (0-11)

            day=calendar.weekday(year,month+1,1) # Get day of week
            month_day_matrix[day, month] += 1

        heatmap_data[year] = month_day_matrix

    return heatmap_data



def spider_plt(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    dayly_times = df.groupby(['day_name']).count()["message"].reset_index()

    return dayly_times


    ##dayly_times = calculate_message_counts(df)

    ##day_indices = [calendar.day_abbr.index(day) for day in df['day_name']]
    ##message_counts = dayly_times['message']

    # Scale message counts (optional)
    ##scaled_counts = message_counts / max(message_counts)

    ##return day_indices, scaled_counts

def get_total_users(selected_user,df):

    if selected_user=="Overall":

        total_users = df['user'].nunique()

        all_users_list = df['user'].unique()

        leave_messages = ["left the group", "left this group", "left"]

        # Create a column indicating whether a message indicates a user leaving
        df['left_group'] = df['message'].str.contains('|'.join(leave_messages), case=False)

        # Get the list of users who left
        users_left_list = df[df['left_group']]['user'].unique()
        users_left_count = len(users_left_list)

        # Calculate the average messages per user
        avg_messages_per_user = df.groupby('user')['message'].count().mean()
        avg_messages_per_user_formatted=round(avg_messages_per_user,2)



        return total_users, users_left_count,avg_messages_per_user_formatted

    return None

























