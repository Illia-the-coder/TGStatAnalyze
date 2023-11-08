import streamlit as st
from backend import *

categoriesDict = {'Цитаты': 'https://uk.tgstat.com/quotes', 'Юмор и развлечения': 'https://uk.tgstat.com/entertainment', 'Политика': 'https://uk.tgstat.com/politics', 'Спорт': 'https://uk.tgstat.com/sport', 'Музыка': 'https://uk.tgstat.com/music', 'Другое': 'https://uk.tgstat.com/other', 'Telegram': 'https://uk.tgstat.com/telegram', 'Софт и приложения': 'https://uk.tgstat.com/apps', 'Блоги': 'https://uk.tgstat.com/blogs', 'Книги': 'https://uk.tgstat.com/books', 'Право': 'https://uk.tgstat.com/law', 'Природа': 'https://uk.tgstat.com/nature', 'Религия': 'https://uk.tgstat.com/religion', 'Картинки и фото': 'https://uk.tgstat.com/pics', 'Интерьер и строительство': 'https://uk.tgstat.com/construction', 'Новости и СМИ': 'https://uk.tgstat.com/news', 'Дизайн': 'https://uk.tgstat.com/design', 'Карьера': 'https://uk.tgstat.com/career', 'Курсы и гайды': 'https://uk.tgstat.com/courses', 'Экономика': 'https://uk.tgstat.com/economics', 'Еда и кулинария': 'https://uk.tgstat.com/food', 'Образование': 'https://uk.tgstat.com/education', 'Букмекерство': 'https://uk.tgstat.com/gambling', 'Криптовалюты': 'https://uk.tgstat.com/crypto', 'Продажи': 'https://uk.tgstat.com/sales', 'Бизнес и стартапы': 'https://uk.tgstat.com/business', 'Лингвистика': 'https://uk.tgstat.com/language', 'Путешествия': 'https://uk.tgstat.com/travels', 'Игры': 'https://uk.tgstat.com/games', 'Транспорт': 'https://uk.tgstat.com/transport', 'Эзотерика': 'https://uk.tgstat.com/esoterics', 'Медицина': 'https://uk.tgstat.com/medicine', 'Для взрослых': 'https://uk.tgstat.com/adult', 'Семья и дети': 'https://uk.tgstat.com/babies', 'Даркнет': 'https://uk.tgstat.com/darknet', 'Инстаграм': 'https://uk.tgstat.com/instagram', 'Здоровье и Фитнес': 'https://uk.tgstat.com/health', 'Видео и фильмы': 'https://uk.tgstat.com/video', 'Технологии': 'https://uk.tgstat.com/tech', 'Маркетинг, PR, реклама': 'https://uk.tgstat.com/marketing', 'Мода и красота': 'https://uk.tgstat.com/beauty', 'Рукоделие': 'https://uk.tgstat.com/handmade', 'Эротика': 'https://uk.tgstat.com/erotica', 'Познавательное': 'https://uk.tgstat.com/edutainment', 'Психология': 'https://uk.tgstat.com/psychology', 'Шок-контент': 'https://uk.tgstat.com/shock', 'Искусство': 'https://uk.tgstat.com/art'}

def fetch_data(selected_category,min_sub):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  result_df = loop.run_until_complete(get_channels_by_category(selected_category,categoriesDict,min_sub))
  return result_df

if __name__ == "__main__":

    selected_category = st.selectbox("Select Category", list(categoriesDict.keys()))
    min_sub = st.number_input("Minimum Subscribers", value = 10000)
    
    include_followers_today = st.checkbox('Подписчики (Сегодня)')
    include_followers_week = st.checkbox('Подписчики (За неделю)')
    include_followers_month = st.checkbox('Подписчики (За месяц)')
  
    citation_index = st.number_input('Индекс цитирования', min_value=0)
    ad_coverage = st.number_input('Средний рекламный охват 1 публикации (За 24 часа)', min_value=0)
  
    channel_age = st.number_input('MAX Возраст канала', value = 1)
  
    if st.button('Run'):
      df = fetch_data(selected_category,min_sub)
      
      # st.dataframe(df)     

      pos_fol = [include_followers_today,include_followers_week,include_followers_month]
      pos_fol = [(1 if x else -1) for x in pos_fol]
      
      df['Возраст канала'] = pd.to_datetime(df['Возраст канала'], format='%d.%m.%Y', errors='coerce')
      current_date = pd.to_datetime('now')
      df['Возраст канала'] = (current_date - df['Возраст канала']).dt.days
      
      df = df[df['Подписчики (Сегодня)'].apply(lambda x: (x/abs(x) if x!=0 else -1)) == pos_fol[0]]
      df = df[df['Подписчики (За неделю)'].apply(lambda x: (x/abs(x) if x!=0 else -1)) == pos_fol[1]]
      df = df[df['Подписчики (За месяц)'].apply(lambda x: (x/abs(x) if x!=0 else -1)) == pos_fol[2]]
      
      df = df[df['Индекс цитирования']>=citation_index]
      df = df[df['Средний рекламный охват 1 публикации (За 24 часа)']>=citation_index]
      df = df[df['Возраст канала']<=channel_age*365]
      
      st.success("Done!")
      st.dataframe(df)     
