import gradio as gr
import requests_html
import pandas as pd
from tqdm import tqdm  # Import tqdm for progress bar

# Define a function to scrape Telegram channels from the given website
def scrape_telegram_channels(url="https://uk.tgstat.com/"):
    """Scrape Telegram channels from the given website.

    Args:
        url: The URL of the website to scrape.

    Returns:
        A DataFrame containing the scraped channel data.
    """

    session = requests_html.HTMLSession()

    response = session.get(url)

    channel_block = response.html.find('body > div.wrapper > div > div.content.p-0.col > div.container-fluid.px-2.px-md-3 > div:nth-child(5) > div > div.card.border.m-0 > div')
    channel_links = list(channel_block[0].absolute_links)

    channels_data = []

    for channel_link in tqdm(channel_links, desc="Scraping Channels"):
        channel_response = session.get(channel_link)
        category_name = channel_response.html.find("h1", first=True).text
        channels_list = channel_response.html.find("#category-list-form > div.row.justify-content-center.lm-list-container > div")

        for channel in channels_list:
            subscribers_count = int(channel.find('div.font-12.text-truncate', first=True).text.replace(' подписчиков', '').replace(' ', ''))
            channel_name = channel.find('div.font-16.text-dark.text-truncate', first=True).text
            link = list(channel.absolute_links)[0]

            if subscribers_count > 10000:
                channels_data.append([channel_name, category_name, subscribers_count, link])

    df = pd.DataFrame(channels_data, columns=['Channel Name', 'Category Name', 'Subscribers', 'Channel Link'])

    return df

# Create a Gradio interface
with gr.Blocks() as interface:
    button = gr.Button("Scrape Channels")

    button.click(scrape_telegram_channels)

    interface.launch()
