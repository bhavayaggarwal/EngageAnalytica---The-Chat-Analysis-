import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
base = "light"
primaryColor = "red"
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose the txt chat file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis WRT", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, avg_words_pertext, num_mediamess, num_links = helper.fetch_stats(selected_user,df)
        col1, col2,col_ex, col3, col4 = st.columns(5)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col_ex:
            st.header("Avg words per text")
            st.title(avg_words_pertext)
        with col3:
            st.header("Total No of media files shared")
            st.title(num_mediamess)
        with col4:
            st.header("Total No of links shared")
            st.title(num_links)
        # finding the most busy user
        if selected_user == "Overall":
            st.markdown("<h1 style='text-align: center; font-size: 30px;'> Top 5 Users with percent chat </h1>",
                        unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            x, df_percent = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical', color="red")
                st.pyplot(fig)
            with col2:
                st.dataframe(df_percent)

        #word cloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
print("This is a test line")


