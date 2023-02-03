import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.set_page_config(page_title="Analyze Before Chat(ABC)")
hide_menu_style="""
               <style>
               #MainMenu {visibility:hidden;}
               footer{visibility:hidden;}
               </style>
                """
#MainMenu {visibility:hidden};
st.markdown(hide_menu_style,unsafe_allow_html=True)
st.sidebar.title(" ABC Analyze Before Chat")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # Converted in String
    # st.text(data)
    df = preprocessor.preprocess(data)

   # st.dataframe(df)

    # Fetch Unique Process

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")  # At 0th position
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, media_messages, links = helper.fetch_stats(selected_user, df)
       # df_wc = helper.create_wordCloud(selected_user, df)
        st.title('Top Analytics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages :")
            st.title(num_messages)
        with col2:
            st.header("Total Words :")
            st.title(words)
        with col3:
            st.subheader("Total Media Shared:")
            st.title(media_messages)
        with col4:
            st.header("Link Shared: ")
            st.title(links)

        # The Monthly TimeLine
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig,animation_frame="time")

        # Daily Timeline here
        st.title("Dailly Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Most Busy Day & Most busy Month
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



        # finding Busiest users from the group
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, neww_df = helper.fetch_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='violet')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(neww_df)

        # Word Cloud

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most - Common - Words
        most_common_df =helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        #st.dataframe(most_common_df)
        st.title("Most Common Words")
        st.pyplot(fig)

        # Emoji Analysis here

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)





