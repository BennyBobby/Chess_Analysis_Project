**Project presentation**

This project is an app created with streamlit in order to analyse et visualise data from chess games of any chess.com player. By writing down a username, the streamlit app generates a dashboard with statistics and key graphs about their performances.


**Key metrics**

- Results distribution
- Ranking evolution
- The most played openings from the user
- Number of games


**Used technologies**

- Python
- Streamlit
- Pandas
- Matplotlib, Seaborn
- Requests
- OS module


**Project structure**

Chess_Analyse_Project/
├── etl/
│   ├── extract_chess_data.py   # Extracts raw data from the API
│   ├── transform_chess_data.py # Transforms JSON data into clean CSV
|   └── main.py                 # ETL pipeline orchestration script
├── data/
│   ├── json/                   # Raw data 
│   └── transformed/            # Processed data
├── visualisation/
│   ├── chess_data_app.py       # The main Streamlit application
│   └── visualisation_utils.py  # Functions for plots and data loading
├── .gitignore
├── README.md
└── requirements.txt 


**How to run the project**

*1-Installation*
pip install -r requirements.txt

*2-Download and process data*
Before running the streamlit application, download and process a player's data. Run the main.py script. It will ask you to enter a Chess.com username.
python etl/main.py

*3-Launch the application*
Once the data has been successfully processed and store in the transformed folder as csv file, launch the Streamlit application.
cd visualisation
streamlit run chess_data_app.py
The application will open in a web browser. Type the same username into the search bar, and the dashboard of the player will be displayed

**sources**

https://support.chess.com/en/articles/9650547-published-data-api 

https://youtu.be/rOBQBUTE3_w?si=qQI9E-20iOk1ZqRx 
