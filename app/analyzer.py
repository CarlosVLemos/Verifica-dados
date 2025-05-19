import pandas as pd
import re
from .translations import gerar_traducao

dataset_path = 'dataset/vazamentos.csv'

def carregar_dataset():
    parse_dates = ['BreachDate', 'AddedDate', 'ModifiedDate']
    return pd.read_csv(dataset_path, parse_dates=parse_dates)

def analisar_risco(nome, email, senha, telefone, cpf=None):
    df = carregar_dataset()
    resultados = []

    if nome and nome.lower() in email.lower():
        resultados.append("O email contém o nome.")
    
    if re.search(r"\d{4}", email):
        resultados.append("O email contém uma data (possível data de nascimento).")

    if df['Nome'].str.lower().str.contains(nome.lower(), na=False).any():
        resultados.append("Nome encontrado em vazamento.")
    if df['Email'].str.lower().str.contains(email.lower(), na=False).any():
        resultados.append("Email encontrado em vazamento.")

    def checar_vazamentos(coluna, valor, label):
        if not valor:
            return
        mask = df[coluna].astype(str).str.lower().str.contains(valor.lower(), na=False)
        for _, row in df[mask].iterrows():
            date_str = row['BreachDate'].date().isoformat()
            resultados.append(f"{label} '{valor}' vazou em '{row['Titulo']}' em {date_str}")

    checar_vazamentos('Nome', nome, 'Nome')
    checar_vazamentos('Email', email, 'Email')
    checar_vazamentos('cpf', cpf, 'CPF')
    checar_vazamentos('telefone', telefone, 'Telefone')

    if not resultados:
        resultados.append("Nenhum risco detectado. Dados parecem seguros.")

    return resultados


def normalizar_dataclasses(dataclasses):
    if pd.isna(dataclasses):
        return ""
    if isinstance(dataclasses, str):
        items = [x.strip().lower() for x in dataclasses.split(',')]
        return ','.join(sorted(set(items)))  # ordena e remove duplicatas
    return dataclasses

def gerar_estatisticas_filtradas(data_ini=None, data_fim=None, dominio=None, tipos=None, verificado=None):
    df = carregar_dataset()


    df['DataClasses'] = df['DataClasses'].apply(normalizar_dataclasses)

    df = df.drop_duplicates()


    if data_ini:
        df = df[df['BreachDate'] >= pd.to_datetime(data_ini)]
    if data_fim:
        df = df[df['BreachDate'] <= pd.to_datetime(data_fim)]


    if dominio:
        df = df[df['Domain'].str.contains(dominio, case=False, na=False)]

 
    if tipos:
        df = df[df['DataClasses'].str.contains('|'.join(tipos), case=False, na=False)]


    if verificado == "True":
        df = df[df['IsVerified'] == True]
    elif verificado == "False":
        df = df[df['IsVerified'] == False]

    stats = {}

    stats['top_domains'] = df['Domain'].value_counts().nlargest(10)


    stats['time_series'] = df.set_index('BreachDate').resample('M').size()


    df = df.drop_duplicates(subset=['Domain', 'DataClasses', 'BreachDate'])
    data_classes = df['DataClasses'].str.split(';').explode()
    stats['data_classes'] = data_classes.value_counts()

    stats['verified'] = df['IsVerified'].value_counts()


    sens_spam = df[['IsSensitive', 'IsSpamList']].apply(lambda col: col.value_counts())
    stats['sensitivity_spam'] = sens_spam

 
    df_exploded = df.copy()
    df_exploded['DataClass'] = df_exploded['DataClasses'].str.split(';')
    df_exploded = df_exploded.explode('DataClass')
    heatmap_df = df_exploded.groupby(['Domain', 'DataClass']).size().unstack(fill_value=0)
    stats['heatmap'] = heatmap_df


    if not df_exploded.empty:
        timeline_df = df_exploded.groupby([
            pd.Grouper(key='BreachDate', freq='M'),
            'DataClass'
        ]).size().unstack(fill_value=0)
    else:
        timeline_df = pd.DataFrame()
    stats['timeline_data_class'] = timeline_df

    return stats, df
