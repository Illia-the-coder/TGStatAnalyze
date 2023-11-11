# ReadMe for Telegram Channel Analysis App
![telegram-cloud-photo-size-2-5354987666313170810-y](https://github.com/Illia-the-coder/TGStatAnalyze/assets/101904816/03e13909-be37-40fc-9a8b-b964e369c37f)

## Overview

This Streamlit-based application provides an intuitive and powerful tool for analyzing Telegram channels. It leverages asynchronous web scraping to gather comprehensive data about various Telegram channels across different categories. The app allows users to filter channels based on subscriber counts and other metrics, providing insights into channel popularity, engagement, and content reach.

## Features

- **Category Selection**: Choose from a wide range of Telegram channel categories such as Politics, Sport, Music, etc.
- **Subscriber Count Filtering**: Set a minimum subscriber threshold to focus on more prominent channels.
- **Metrics Analysis**: Analyze channels based on daily, weekly, and monthly subscriber changes, citation index, average advertising reach per post, and channel age.
- **Data Visualization**: View the data in a structured and easy-to-read format directly within the app.
- **Asynchronous Data Fetching**: Fast and efficient data scraping with asynchronous requests.

## Installation

Before you begin, ensure you have Python installed on your system. This app requires Python 3.7 or later.

1. **Clone the Repository**:
   ```
   git clone https://github.com/Illia-the-coder/TGStatAnalyze.git
   cd telegram-channel-analysis
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app using the following command:

```
streamlit run app.py
```

Navigate to the displayed URL in your web browser to use the application.

## App Interface

- **Select Category**: Choose a category from the dropdown menu.
- **Minimum Subscribers**: Enter the minimum number of subscribers for the channels to be included.
- **Subscriber Growth Filters**: Check the boxes to include channels based on daily, weekly, or monthly subscriber growth.
- **Additional Filters**: Set the citation index, advertising reach, and maximum channel age as per your analysis needs.
- **Run Analysis**: Click the 'Run' button to fetch and display the data.

## Contributing

Contributions are welcome! Please read our contributing guidelines to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



---

Remember to replace placeholders like GitHub repository links, email addresses, etc., with your actual information. Also, ensure that all the necessary files such as `requirements.txt` and `LICENSE` are present in your repository.
