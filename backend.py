import os
import asyncio
from requests_html import AsyncHTMLSession
import logging
import pandas as pd
import json
import streamlit as st

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

async def get_dict_topic():
    asession = AsyncHTMLSession()
    response = await asession.get('https://uk.tgstat.com/', headers=headers)
    category_block = response.html.find('body > div.wrapper > div > div.content.p-0.col > div.container-fluid.px-2.px-md-3 > div:nth-child(5) > div > div.card.border.m-0 > div')
    category_links = list(category_block[0].absolute_links)
    category_names = []

    for category_link in tqdm(category_links, desc='Fetching Categories', ncols=100):
        try:
            response = await asession.get(category_link, headers=headers)
            name = response.html.find("h1", first=True).text
            category_names.append(name)
        except Exception as e:
            print(f"Error fetching data from {category_link}: {e}")

    return dict(zip( category_names,category_links))

if not os.path.exists('categories.json'):
    categoriesDict = asyncio.get_event_loop().run_until_complete(get_dict_topic())
    with open('categories.json', 'w') as f:
        f.write(json.dumps(categoriesDict))

async def get_channels_by_category(category_name):
    asession = AsyncHTMLSession()

    with open('categories.json', 'r') as f:
        categoriesDict = eval(f.read())
    category_link = categoriesDict[category_name]

    logging.info(f'Fetching data from {category_link}')

    response = await asession.get(category_link, headers=headers)
    channels_list = response.html.find("#category-list-form > div.row.justify-content-center.lm-list-container > div")
    channels_data = []
    progress_text = "Parsing..."
    my_bar = st.progress(0, text=progress_text)
  
    for index,channel in enumerate(channels_list):
        channel_name = channel.find('div.font-16.text-dark.text-truncate', first=True).text
        Tgstat_link = str(list(channel.absolute_links)[0]) +'/stat'

        async def get_values_by_channel(stats_link):
            r = await asession.get(stats_link, headers=headers)
            r = r.html
            subscribers_count = int(r.find("#sticky-center-column > div > div > div:nth-child(1) > div > h2", first=True).text.replace(' ', ''))

            chatBlock = r.find("#sticky-center-column > div > div > div > div > div.position-absolute.text-uppercase.text-dark.font-12")
            chars = [x.text.replace('\n',' ').capitalize() for x in chatBlock]
            allBlocks = r.find('#sticky-center-column > div > div > div > div')
            allText = [x.text.split('\n') for x in allBlocks ]
            dict_ = dict(zip(chars, allText))
            required_columns = ['Подписчики', 'Индекс цитирования','Средний охват 1 публикации','Средний рекламный охват 1 публикации','Возраст канала']
            for key in dict_.keys():
              if key not in required_columns:
                try:
                  dict_[key]=eval(dict_[key][0].replace(' ', '').replace('всего',' ').replace('%','/100').replace('k','*1000'))
                except:
                  pass

            def process_metric(metric, keys, transformations, mainKey):
                for i in range(1, len(metric)):
                    if metric[i] in keys:
                        key = metric[i].capitalize()
                        try:
                          value = round(eval(metric[i - 1].replace(' ', '').replace('%', '/100').replace('k', '*1000')),2) if metric[i] != 'канал создан' else metric[i - 1]
                        except:
                          value = None
                        transformations[f'{mainKey} ({key})'] = value

            keys_and_transformations = {
                'Подписчики': ['сегодня', 'за неделю', 'за месяц'],
                'Индекс цитирования': ['уп. каналов', 'упоминаний', 'репостов'],
                'Средний охват 1 публикации': ['ERR', 'ERR24'],
                'Средний рекламный охват 1 публикации': ['за 12 часов', 'за 24 часа', 'за 48 часов'],
                'Возраст канала': ['канал создан']
            }

            for key, values in keys_and_transformations.items():
                process_metric(dict_[key], values, dict_,key)


            for key in dict_.keys():
              if key in required_columns and key != 'Возраст канала':
                try:
                  dict_[key]=eval(dict_[key][0].replace(' ', '').replace('всего',' ').replace('%','/100').replace('k','*1000'))
                except:
                  pass
            del dict_['Возраст канала']
            dict_['TG Link'] = list(r.find('body > div.wrapper > div > div.content.p-0.col > div.container-fluid.px-2.px-md-3 > div:nth-child(2) > div > div > div > div.col-12.col-sm-7.col-md-8.col-lg-6 > div.text-center.text-sm-left > a')[0].absolute_links)[0]
            return dict_


        subscribers_count = int(channel.find('div.font-12.text-truncate', first=True).text.replace(' подписчиков', '').replace(' ', ''))
        if subscribers_count > 10000:
          values = await get_values_by_channel(Tgstat_link)
          values['Name'] = channel_name
          values['Tgstat_link'] = Tgstat_link

          channels_data.append(values)
          
        my_bar.progress((index + 1)/len(channels_list), text=progress_text)
    
    df = pd.DataFrame(channels_data)
    df = df.rename(columns={'Возраст канала (Канал создан)': 'Канал создан'})
    # df['Канал создан'] = pd.to_datetime(df['Канал создан'], format='%d.%m.%Y', errors='coerce')
    desired_column_order = [
      'Name', 'TG Link', 'Tgstat_link','Канал создан',
      'Подписчики', 'Индекс цитирования', 'Средний охват 1 публикации',
      'Средний рекламный охват 1 публикации', 'Публикации',
      'Вовлеченность подписчиков (err)', 'Вовлеченность подписчиков (er)',
      'Подписчики (Сегодня)', 'Подписчики (За неделю)',
      'Подписчики (За месяц)', 'Индекс цитирования (Уп. каналов)',
      'Индекс цитирования (Упоминаний)', 'Индекс цитирования (Репостов)',
      'Средний охват 1 публикации (Err)',
      'Средний охват 1 публикации (Err24)',
      'Средний рекламный охват 1 публикации (За 12 часов)',
      'Средний рекламный охват 1 публикации (За 24 часа)',
      'Средний рекламный охват 1 публикации (За 48 часов)',
       'Подписки/отписки за 24 часа',
      'Пол подписчиков', 'Stories'
    ]
    desired_column_order = [x for x in desired_column_order if x in df.columns]

    # Reorder the columns in the DataFrame
    df = df[desired_column_order]

    # Save the DataFrame to CSV file
    df.to_csv(f'{category_name}.csv', index=False)
    return df



