import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import helper
import preprocessor
import calendar
import plotly.express as pr




st.sidebar.title("Whatsapp chat analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)



    user_list = df["user"].unique().tolist()
    user_list.remove("group notifications")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("View user", user_list)

    if st.sidebar.button("Show analysis"):

        num_messgaes, words, num_media_msg, links = helper.fetch_stats(selected_user,df)
        st.title("TOP STATISTICS")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messgaes)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total media")
            st.title(num_media_msg)
        with col4:
            st.header("Links Shared")
            st.title(links)

        # Users
        if selected_user == "Overall":
            total_users,users_left,avg_msg=helper.get_total_users(selected_user, df)

            st.title("Users")
            col1,col2,col3=st.columns(3)

            with col1:
                st.header("No of users")
                st.title(total_users)
            with col2:
                st.header("Users left")
                st.title(users_left)
            with col3:
                st.header("Av.Msg/User")
                st.title(avg_msg)


        # monthly_timeline
        sns.set_style("dark")
        st.title("Monthly timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="red")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily_timeline
        sns.set_style("darkgrid")
        st.title("Daily timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline["date_only"], daily_timeline["message"],color="red")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)






        # activity map
        st.title("Activity map")

        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        col3,col4=st.columns(2)

        with col3:
            # sorted daily_timeline_desc
            st.title("Highest active date")
            sorted_daily_timeline=helper.sorted_timeline_desc(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(sorted_daily_timeline["date_only"].astype(str),sorted_daily_timeline["message"])
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col4:
            st.header("Most busy year")
            busy_year=helper.highest_years(selected_user,df)
            busy_year.index=busy_year.index.astype(int)
            fig,ax=plt.subplots()
            ax.bar(busy_year.index,busy_year.values,color="orange")
            plt.xticks(rotation=45)
            st.pyplot(fig)


        st.title("Weekly activity map")
        users_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(users_heatmap)
        st.pyplot(fig)




        # finding the most busiest users

        if selected_user == "Overall":
            st.title("Most busy users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 , col3 = st.columns(3)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            with col3:
                fig, ax = plt.subplots(figsize=(10,10))
                labels = new_df["name"].head()
                color_map = plt.cm.get_cmap('tab10', len(labels))
                ax.pie(new_df["percent"].head(), labels=labels, autopct='%0.2f', startangle=90, colors=color_map.colors)
                st.pyplot(fig)

        # Wordcloud

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most common words")
        return_df = helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(return_df)
        with col2:
             ax.barh(return_df[0], return_df[1], color='red')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

        # Emoji analysis

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("emoji analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # donut chart

            fig,ax=plt.subplots(figsize=(10,10))
            colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','gray']
            labels=emoji_df[0].head()
            explode = (0.05, 0.05, 0.05, 0.05, 0.05)
            ax.pie(emoji_df[1].head(), labels=labels,autopct="%0.2f",  pctdistance=0.85, colors=colors, explode=explode)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            st.pyplot(fig)

        # some more stats

        st.title("Some more stats")

        msgs_per_hour,words_per_msg,avg_msg_length=helper.msgs_per_hour(selected_user,df)

        col1,col2,col3=st.columns(3)

        with col1:

            st.header("msgs/hour")
            st.title(msgs_per_hour)

        with col2:
            st.header("words/msg")
            st.title(words_per_msg)

        with col3:
            st.header("Avg msg length")
            st.title(avg_msg_length)

        # calender heatmap

        sns.set()

        st.title("Calender heatmap")



        heatmap_data= helper.calender_heatmap(selected_user,df)

        # Create a subplot


        for(year, year_data) in heatmap_data.items():

            year_data_int = year_data.astype(int)

            fig, ax = plt.subplots(figsize=(10,6))

            ax.set_title(f'Contributions Calendar for {year}')

            # Create the heatmap
            sns.heatmap(year_data_int, annot=False,fmt='d',  cmap='Reds', ax=ax)


            ax.set_title(f'Year {year} ')

            ax.set_xticklabels(calendar.month_abbr[1:])


            ax.set_yticks([])


            # Adjust layout
            plt.tight_layout()


            # Convert the plot to an image
            st.pyplot(fig)


        #spider plot

        st.title("Spider Plot ")

        dayly_times=helper.spider_plt(selected_user,df)

        # Create a spider plot using Plotly
        fig = pr.line_polar(
        dayly_times,
        r="message",
        theta="day_name",
        line_close=True,
        title=f"Spider Plot for {selected_user}",
        )

        # Update the layout to make it look like a spider plot
        fig.update_polars(radialaxis_tickvals=[0], radialaxis_ticktext=[""],  radialaxis_showgrid=True,radialaxis_gridcolor='gray',
        radialaxis_gridwidth=2 )
        fig.update_traces(fill="toself")



        # Display the plot using Streamlit
        st.plotly_chart(fig)




















