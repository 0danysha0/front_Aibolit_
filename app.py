# app.py
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Путь к вашему файлу с данными
data_file_path = 'out.csv'

# Загрузка данных из файла в DataFrame
data_df = pd.read_csv(data_file_path)

def predict_ic50(smiles):
    # Здесь вы можете использовать вашу логику предсказания IC50 на основе SMILES
    # В данном случае, заглушка в виде текста "It's IC50 results"
    return "It's IC50 results"

def find_smiles_data(smiles):
    # Поиск данных в DataFrame по SMILES
    result_df = data_df[data_df['smiles'] == smiles]
    
    # Если SMILES найден, вернем DataFrame с данными
    if not result_df.empty:
        return result_df.iloc[:, 1:]  # Исключаем столбец с SMILES
    else:
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если SMILES не найден

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        smiles_input = request.form['smilesInput']
        
        # Вызовем функцию для поиска данных по SMILES
        smiles_data = find_smiles_data(smiles_input)
        
        if not smiles_data.empty:
            # Если есть данные по SMILES, преобразуем их в HTML-таблицу
            table_html = smiles_data.to_html(classes='table table-bordered', index=False)
        else:
            table_html = "No data found for the entered SMILES."
        
        # Вызовем функцию для предсказания IC50
        ic50_result = predict_ic50(smiles_input)
        
        return render_template('index.html', result=ic50_result, smiles_input=smiles_input, table=table_html)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

