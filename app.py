import pandas as pd
import gradio as gr
from requests_html import HTMLSession

# Define a function to perform the scraping and return the DataFrame
def scrape_channels():
    session = HTMLSession()

    # Send a GET request to the website
    response = session.get('https://uk.tgstat.com/')

    # Find the specific HTML block containing channel links
    channel_block = response.html.find('body > div.wrapper > div > div.content.p-0.col > div.container-fluid.px-2.px-md-3 > div:nth-child(5) > div > div.card.border.m-0 > div')
    channel_links = list(channel_block[0].absolute_links)

    # Initialize an empty list to store channel data
    channels_data = []

    for channel_link in channel_links:
        channel_response = session.get(channel_link)
        category_name = channel_response.html.find("h1", first=True).text
        channels_list = channel_response.html.find("#category-list-form > div.row.justify-content-center.lm-list-container > div")

        for channel in channels_list:
            subscribers_count = int(channel.find('div.font-12.text-truncate', first=True).text.replace(' подписчиков', '').replace(' ', ''))
            channel_name = channel.find('div.font-16.text-dark.text-truncate', first=True).text
            link = list(channel.absolute_links)[0]

            if subscribers_count > 10000:
                channels_data.append([channel_name, category_name, subscribers_count, link])

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(channels_data, columns=['Channel Name', 'Category Name', 'Subscribers', 'Channel Link'])
    return df

# Create a Gradio interface with a button to trigger the scraping and a function output
iface = gr.Interface(fn=scrape_channels,
                     outputs=gr.Dataframe(),
                     live=True, )

# Launch the Gradio app
iface.launch()
