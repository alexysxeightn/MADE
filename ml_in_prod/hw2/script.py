import json
import pandas as pd
import requests


if __name__ == '__main__':
    df = pd.read_csv('data/raw/heart_cleveland_upload.csv').drop('condition', axis=1)
    df['id'] = range(len(df))
    data = df.to_dict('records')
    response = requests.post('http://localhost:8000/predict', data=json.dumps(data))

    print(f'Сэмпл из данных: {data[0]} \n')
    print(f'Status code: {response.status_code} \n')
    print(f'Ответ сервиса (первые 10 сэмплов): {response.json()[:10]}')
