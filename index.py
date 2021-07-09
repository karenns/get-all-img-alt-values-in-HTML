# SQL
# SELECT * from wpvw_posts where post_type in ('post','page') and post_status = 'publish'

# Library
import pandas as pd
import bs4 
#from urllib.parse import urlsplit

# Open CSV
df = pd.read_csv('wpvw_posts.csv', header=None)

# Get rid of all columns except id, post_name, post_content
df = df[[0,4,11]]

# Name the columns
df.columns = ['id', 'post_content', 'post_name']

# Add new column with full url
df['url'] = 'https://website.com/' + df['post_name']

# Make it smaller just for TESTING purposes
#df = df.loc[1:10]


# Get only images
def show_imgSRC(row):
    post_id = row['id']
    html = row['post_content']
    url = row['url']
    img_lst = []
    
    if not pd.isnull(html):
        soup = bs4.BeautifulSoup(html, "html.parser")
        for img in soup.find_all('img'):
            try:
                altImg = img['alt']
                if (altImg == ''):
                    img_lst.append(img)
            except:
                img_lst.append(img)
       #print(img_lst)
    return img_lst


# From each row - Get all images
df['images'] = df.apply(show_imgSRC, axis=1)

# Get rid of the column except post_content
df = df[['id','url','images']]

# Filter dataframe to remove rows without images
#df_filtered = df[len(df['images']) >0]

df_filtered = df[df['images'].apply(lambda x: len(x)) > 0]

#print(df_filtered.head())

# Export CSV
df_filtered.to_csv('output.csv',index=False)