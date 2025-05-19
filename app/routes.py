from flask import Blueprint, render_template, request
import pandas as pd
from .analyzer import analisar_risco, gerar_estatisticas_filtradas, carregar_dataset
import plotly.graph_objs as go
import plotly.io as pio
from .translations import gerar_traducao, traduzir_texto_composto

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    riscos = []
    if request.method == 'POST':
        nome     = request.form.get('nome', '')
        email    = request.form.get('email', '')
        senha    = request.form.get('senha', '')
        telefone = request.form.get('telefone', '')
        cpf      = request.form.get('cpf', '')
        riscos   = analisar_risco(nome, email, senha, telefone, cpf)
    return render_template('formulario.html', riscos=riscos)

@bp.route('/dashboard')
def dashboard():
    # --- Filtros via GET ---
    data_ini = request.args.get('data_inicial')
    data_fim = request.args.get('data_final')
    dominio  = request.args.get('dominio')
    tipos    = request.args.getlist('tipos')
    verif    = request.args.get('verificado')

    stats, df_filtrado = gerar_estatisticas_filtradas(
        data_ini, data_fim, dominio, tipos, verif
    )

    traducoes_completas = gerar_traducao()

    stats['data_classes'].index = [
        ', '.join(item.strip().title() for item in idx.split(',')) for idx in stats['data_classes'].index
    ]
    stats['data_classes'].rename(index=traducoes_completas, inplace=True)

    df_filtrado['DataClasses'] = df_filtrado['DataClasses'].fillna('')
    df_filtrado = df_filtrado[df_filtrado['DataClasses'] != '']
    df_filtrado['DataClasses'] = df_filtrado['DataClasses'].apply(
        lambda x: traduzir_texto_composto(x, traducoes_completas)
    )

    map_data_classes = {
        'Passwords': 'Senhas',
        'Phone Numbers': 'Números de Telefone',
        'Email Address': 'Endereço de Email',
        'Email Addresses': 'Endereços de Email',
        'Physical Addresses': 'Endereços Físicos',
        'Usernames': 'Nomes de Usuário',
    }

    # --- Gráfico 1 ---
    fig_top = go.Figure([go.Bar(
        x=stats['top_domains'].index,
        y=stats['top_domains'].values
    )])
    fig_top.update_layout(
        title='Vazamentos por Domínio',
        xaxis_title='Domínio',
        yaxis_title='Quantidade'
    )
    chart_top_domains = pio.to_html(fig_top, full_html=False)

    # --- Gráfico 2 ---
    fig_ts = go.Figure([go.Scatter(
        x=stats['time_series'].index,
        y=stats['time_series'].values,
        mode='lines+markers'
    )])
    fig_ts.update_layout(
        title='Vazamentos ao Longo do Tempo (Mensal)',
        xaxis_title='Data',
        yaxis_title='Número de Vazamentos'
    )
    chart_time_series = pio.to_html(fig_ts, full_html=False)

    # --- Gráfico 3 (Com tradução completa de rótulos compostos) ---
    tipo_df = df_filtrado.copy()
    data_classes_stats = tipo_df['DataClasses'].value_counts()

    def traduzir_composto(label):
        partes = [p.strip() for p in label.split(',')]
        traduzidas = [map_data_classes.get(p.title(), p.title()) for p in partes]
        return ', '.join(traduzidas)

    data_classes_traduzidos = [traduzir_composto(item) for item in data_classes_stats.index]

    fig_data_classes = go.Figure([go.Bar(
        x=data_classes_traduzidos,
        y=data_classes_stats.values
    )])
    fig_data_classes.update_layout(
        title='Distribuição por Tipo de Dado Vazado',
        xaxis_title='Tipo de Dado',
        yaxis_title='Contagem'
    )
    chart_data_classes = pio.to_html(fig_data_classes, full_html=False)

    # --- Gráfico 4 ---
    vc = stats['verified']
    fig_verified = go.Figure([go.Bar(
        x=['Verificado', 'Não Verificado'],
        y=[vc.get(True, 0), vc.get(False, 0)]
    )])
    fig_verified.update_layout(
        title='Status de Verificação dos Registros',
        xaxis_title='Status',
        yaxis_title='Quantidade'
    )
    chart_verified = pio.to_html(fig_verified, full_html=False)

    # --- Gráfico 5 ---
    ss = stats['sensitivity_spam']
    fig_sensitive = go.Figure([
        go.Bar(name='Sensível', x=['Sim', 'Não'], y=[ss.loc[True, 'IsSensitive'] if True in ss.index else 0, ss.loc[False, 'IsSensitive'] if False in ss.index else 0]),
        go.Bar(name='Spam', x=['Sim', 'Não'], y=[ss.loc[True, 'IsSpamList'] if True in ss.index else 0, ss.loc[False, 'IsSpamList'] if False in ss.index else 0])
    ])
    fig_sensitive.update_layout(
        title='Sensibilidade e Spam nos Registros',
        barmode='group',
        xaxis_title='Condição',
        yaxis_title='Quantidade'
    )
    chart_sensitive = pio.to_html(fig_sensitive, full_html=False)

    # --- Gráfico 6 ---
    heat_df = df_filtrado.copy()
    heat_df = heat_df.assign(
        DataClasses=heat_df['DataClasses'].apply(lambda x: sorted(set(i.strip() for i in x.split(',') if i.strip())))
    )
    heat_df = heat_df.explode('DataClasses')
    heat_df = heat_df[heat_df['DataClasses'] != '']

    heat = pd.crosstab(heat_df['Domain'], heat_df['DataClasses'])
    heat = heat.sort_index()
    heat = heat[sorted(heat.columns)]

    heat.columns = [map_data_classes.get(col.title(), col.title()) for col in heat.columns]

    fig_stacked = go.Figure()
    for col in heat.columns:
        fig_stacked.add_trace(go.Bar(name=col, x=heat.index, y=heat[col]))

    fig_stacked.update_layout(
        barmode='stack',
        title='Distribuição de Tipos de Dados por Domínio',
        xaxis_title='Domínio',
        yaxis_title='Quantidade',
        legend_title='Tipo de Dado'
    )
    chart_heatmap = pio.to_html(fig_stacked, full_html=False)

    # --- Gráfico 7 ---
    line_df = df_filtrado.copy()
    line_df = line_df.assign(
        DataClasses=line_df['DataClasses'].apply(lambda x: sorted(set(i.strip() for i in x.split(',') if i.strip())))
    )
    line_df = line_df.explode('DataClasses')
    line_df = line_df[line_df['DataClasses'] != '']

    line_df['BreachMonth'] = line_df['BreachDate'].dt.to_period('M').dt.to_timestamp()
    timeline = line_df.groupby(['BreachMonth', 'DataClasses']).size().unstack().fillna(0)

    timeline.columns = [map_data_classes.get(col.title(), col.title()) for col in timeline.columns]
    timeline = timeline[sorted(timeline.columns)]

    fig_timeline = go.Figure()
    for col in timeline.columns:
        fig_timeline.add_trace(go.Scatter(
            x=timeline.index,
            y=timeline[col],
            mode='lines',
            name=col
        ))
    fig_timeline.update_layout(
        title='Timeline por Tipo de Dado Vazado',
        xaxis_title='Data',
        yaxis_title='Quantidade'
    )
    chart_timeline_classes = pio.to_html(fig_timeline, full_html=False)

    df = carregar_dataset()
    dominios_disponiveis = sorted(df['Domain'].dropna().unique())
    tipos_disponiveis = sorted(set(';'.join(df['DataClasses'].dropna()).split(';')))

    return render_template(
        'dashboard.html',
        stats=stats,
        chart_top_domains=chart_top_domains,
        chart_time_series=chart_time_series,
        chart_data_classes=chart_data_classes,
        chart_verified=chart_verified,
        chart_sensitive=chart_sensitive,
        chart_heatmap=chart_heatmap,
        chart_timeline_classes=chart_timeline_classes,
        filtros={
            'data_ini': data_ini,
            'data_fim': data_fim,
            'dominio': dominio,
            'tipos': tipos,
            'verif': verif,
            'dominios_disponiveis': dominios_disponiveis,
            'tipos_disponiveis': tipos_disponiveis,
        }
    )
