import streamlit as st
from backend import *

categoriesDict = {'Цитаты': 'https://uk.tgstat.com/quotes', 'Юмор и развлечения': 'https://uk.tgstat.com/entertainment', 'Политика': 'https://uk.tgstat.com/politics', 'Спорт': 'https://uk.tgstat.com/sport', 'Музыка': 'https://uk.tgstat.com/music', 'Другое': 'https://uk.tgstat.com/other', 'Telegram': 'https://uk.tgstat.com/telegram', 'Софт и приложения': 'https://uk.tgstat.com/apps', 'Блоги': 'https://uk.tgstat.com/blogs', 'Книги': 'https://uk.tgstat.com/books', 'Право': 'https://uk.tgstat.com/law', 'Природа': 'https://uk.tgstat.com/nature', 'Религия': 'https://uk.tgstat.com/religion', 'Картинки и фото': 'https://uk.tgstat.com/pics', 'Интерьер и строительство': 'https://uk.tgstat.com/construction', 'Новости и СМИ': 'https://uk.tgstat.com/news', 'Дизайн': 'https://uk.tgstat.com/design', 'Карьера': 'https://uk.tgstat.com/career', 'Курсы и гайды': 'https://uk.tgstat.com/courses', 'Экономика': 'https://uk.tgstat.com/economics', 'Еда и кулинария': 'https://uk.tgstat.com/food', 'Образование': 'https://uk.tgstat.com/education', 'Букмекерство': 'https://uk.tgstat.com/gambling', 'Криптовалюты': 'https://uk.tgstat.com/crypto', 'Продажи': 'https://uk.tgstat.com/sales', 'Бизнес и стартапы': 'https://uk.tgstat.com/business', 'Лингвистика': 'https://uk.tgstat.com/language', 'Путешествия': 'https://uk.tgstat.com/travels', 'Игры': 'https://uk.tgstat.com/games', 'Транспорт': 'https://uk.tgstat.com/transport', 'Эзотерика': 'https://uk.tgstat.com/esoterics', 'Медицина': 'https://uk.tgstat.com/medicine', 'Для взрослых': 'https://uk.tgstat.com/adult', 'Семья и дети': 'https://uk.tgstat.com/babies', 'Даркнет': 'https://uk.tgstat.com/darknet', 'Инстаграм': 'https://uk.tgstat.com/instagram', 'Здоровье и Фитнес': 'https://uk.tgstat.com/health', 'Видео и фильмы': 'https://uk.tgstat.com/video', 'Технологии': 'https://uk.tgstat.com/tech', 'Маркетинг, PR, реклама': 'https://uk.tgstat.com/marketing', 'Мода и красота': 'https://uk.tgstat.com/beauty', 'Рукоделие': 'https://uk.tgstat.com/handmade', 'Эротика': 'https://uk.tgstat.com/erotica', 'Познавательное': 'https://uk.tgstat.com/edutainment', 'Психология': 'https://uk.tgstat.com/psychology', 'Шок-контент': 'https://uk.tgstat.com/shock', 'Искусство': 'https://uk.tgstat.com/art'}

def fetch_data(selected_category):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  result_df = loop.run_until_complete(get_channels_by_category(selected_category))
  return result_df

if __name__ == "__main__":

    selected_category = st.selectbox("Select Category", list(categoriesDict.keys()))

    if st.button('Run'):
      df = fetch_data(selected_category)
      st.success("Done!")
      st.dataframe(df)     
