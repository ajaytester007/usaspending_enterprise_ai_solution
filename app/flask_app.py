from pathlib import Path
import json
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
GOLD_CSV = Path('data/gold/state_quarter_summary.csv')
METADATA = Path('config/metadata_catalog.json')

@app.route("/favicon.ico")
def favicon():
    return "", 204

def load_data():
    if GOLD_CSV.exists():
        return pd.read_csv(GOLD_CSV)
    fallback = Path('data/silver/state_quarter_spend.csv')
    if fallback.exists():
        return pd.read_csv(fallback)
    return pd.DataFrame(columns=['state','year','quarter','period','total_obligations','transaction_count'])

@app.route('/')
def index():
    df = load_data()
    states = sorted(df['state'].dropna().unique().tolist()) if not df.empty else []
    return render_template('index.html', states=states)

@app.route('/api/summary')
def api_summary():
    df = load_data()
    state = request.args.get('state')
    if state:
        df = df[df['state'] == state]
    return jsonify({
        'rows': int(len(df)),
        'total_obligations': float(df['total_obligations'].sum()) if not df.empty else 0,
        'transaction_count': int(df['transaction_count'].sum()) if not df.empty else 0,
        'states': sorted(df['state'].dropna().unique().tolist()) if not df.empty else []
    })

@app.route('/charts')
def charts():
    df = load_data()
    state = request.args.get('state')
    if state:
        df = df[df['state'] == state]
    if df.empty:
        return '<h2>No data yet. Run python scripts/run_local.py first.</h2>'
    fig1 = px.line(df.sort_values(['year','quarter']), x='period', y='total_obligations', color='state', markers=True, title='Quarterly Federal Obligations')
    state_summary = df.groupby('state', as_index=False)['total_obligations'].sum().sort_values('total_obligations', ascending=False)
    fig2 = px.bar(state_summary, x='state', y='total_obligations', title='Spend by State')
    return render_template('charts.html', chart1=fig1.to_html(full_html=False), chart2=fig2.to_html(full_html=False), table=df.to_html(classes='table table-striped', index=False))

@app.route('/metadata')
def metadata():
    catalog = json.loads(METADATA.read_text()) if METADATA.exists() else {}
    return render_template('metadata.html', catalog=json.dumps(catalog, indent=2))

@app.route('/designer')
def designer():
    return render_template('designer.html')

@app.route('/agent')
def agent():
    return render_template('agent.html')

@app.route('/api/agent/query', methods=['POST'])
def agent_query():
    question = request.json.get('question','')
    # Safe starter: deterministic response over local data. Replace with LLM + RAG later.
    df = load_data()
    total = float(df['total_obligations'].sum()) if not df.empty else 0
    return jsonify({
        'question': question,
        'answer': f'Local RAG/Agent scaffold active. Current curated dataset has {len(df)} records and total obligations ${total:,.0f}. Add vector index + LLM key to enable semantic retrieval.',
        'sources': ['data/gold/state_quarter_summary.csv', 'config/metadata_catalog.json']
    })

if __name__ == '__main__':
    app.run(debug=True)
