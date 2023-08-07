from wordcloud import WordCloud
def fetch_stats(selected_user, df):
    from urlextract import URLExtract
    extractor=URLExtract()
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    num_messages = df.shape[0]
    words = []
    for mess in df["messages"]:
        words.extend(mess.split())
    num_mediamess = df[df["messages"] == "<Media omitted>"].shape[0]
    links = []
    for mess in df["messages"]:
        links.extend(extractor.find_urls(mess))
    
    return num_messages, len(words), round(len(words) / num_messages,2), num_mediamess, len(links)
    # fetch no of media sent

def most_busy_users(df):
    import matplotlib.pyplot as plt
    x = df["users"].value_counts().head()
    df_percent = round((df["users"].value_counts().head()/df.shape[0]*100), 2).reset_index().rename(columns={"index":"name","users":"percent"})
    return x,df_percent


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    wc = WordCloud(min_font_size=10,background_color='pink')
    df_wc = wc.generate(df["messages"].str.cat(sep=""))
    return df_wc
