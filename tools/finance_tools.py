import json
from datetime import datetime, timedelta
from typing import Dict, List, Union

def calculate_portfolio_metrics(portfolio_data: str) -> str:
    """
    Calcula métricas importantes de uma carteira de investimentos.
    
    Args:
        portfolio_data: JSON string com dados da carteira no formato:
        {"assets": [{"symbol": "AAPL", "quantity": 10, "avg_price": 150}]}
        
    Returns:
        String com análise da carteira formatada em markdown
    """
    try:
        data = json.loads(portfolio_data)
        assets = data.get("assets", [])
        
        if not assets:
            return "❌ Nenhum ativo fornecido na carteira."
        
        output = "# 📊 Análise de Carteira de Investimentos\n\n"
        output += f"*Análise realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n"
        
        total_invested = 0
        output += "## 💼 Posições da Carteira\n\n"
        output += "| Ativo | Quantidade | Preço Médio | Investido |\n"
        output += "|-------|------------|-------------|------------|\n"
        
        for asset in assets:
            symbol = asset.get("symbol", "N/A")
            quantity = asset.get("quantity", 0)
            avg_price = asset.get("avg_price", 0)
            invested = quantity * avg_price
            total_invested += invested
            
            output += f"| {symbol} | {quantity} | ${avg_price:.2f} | ${invested:.2f} |\n"
        
        output += f"\n**💰 Total Investido:** ${total_invested:,.2f}\n\n"
        
        # Métricas básicas
        output += "## 📈 Métricas Calculadas\n\n"
        output += f"• **Número de Ativos:** {len(assets)}\n"
        output += f"• **Investimento Total:** ${total_invested:,.2f}\n"
        output += f"• **Maior Posição:** ${max([a['quantity'] * a['avg_price'] for a in assets]):,.2f}\n"
        output += f"• **Menor Posição:** ${min([a['quantity'] * a['avg_price'] for a in assets]):,.2f}\n\n"
        
        # Concentração
        output += "## ⚖️ Análise de Concentração\n\n"
        for asset in assets:
            weight = (asset['quantity'] * asset['avg_price']) / total_invested * 100
            risk_level = "🔴 Alto" if weight > 40 else "🟡 Médio" if weight > 20 else "🟢 Baixo"
            output += f"• **{asset['symbol']}:** {weight:.1f}% - Risco: {risk_level}\n"
        
        output += "\n## 💡 Recomendações\n\n"
        output += "• Use as ferramentas YFinance ou OpenBB para obter preços atuais\n"
        output += "• Considere rebalanceamento se algum ativo > 40% da carteira\n"
        output += "• Monitore correlação entre ativos para diversificação\n\n"
        
        output += "---\n"
        output += "**⚠️ Disclaimer:** Esta análise é apenas educacional e não constitui recomendação de investimento."
        
        return output
        
    except json.JSONDecodeError:
        return "❌ Erro: Formato JSON inválido. Use: {\"assets\": [{\"symbol\": \"AAPL\", \"quantity\": 10, \"avg_price\": 150}]}"
    except Exception as e:
        return f"❌ Erro ao calcular métricas: {str(e)}"
