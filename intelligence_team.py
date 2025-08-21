from agno.agent import Agent
from agno.team import Team
from agno.tools.tavily import TavilyTools
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.youtube import YouTubeTools
from agno.tools.browserbase import BrowserbaseTools
# from agno.tools.firecrawl import FirecrawlTools
from agno.tools.website import WebsiteTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.x import XTools
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from tools.finance_tools import calculate_portfolio_metrics
from datetime import datetime

# Configurar memória compartilhada
memory = Memory(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=SqliteMemoryDb(table_name="team_memories", db_file="tmp/team_memory.db")
)

# ============================================================================
# AGENTE DE TECNOLOGIA E IA
# ============================================================================
tech_ai_agent = Agent(
    name="TechAI_Specialist",
    model=OpenAIChat(id="gpt-4.1-mini"),
    role="Especialista em tecnologia, programação e inteligência artificial",
    tools=[
        TavilyTools(search_depth="advanced", max_tokens=8000),
        XTools(wait_on_rate_limit=True, include_post_metrics=True),
        WebsiteTools(),
        YouTubeTools()
    ],
    instructions=f"""
    {open("prompts/tech_agent.md").read()}
    
    IMPORTANTE: Hoje é {datetime.now().strftime('%d de %B de %Y')}. 
    """,
    memory=memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=5,
    show_tool_calls=True,
    storage=SqliteStorage(table_name="tech_agent_sessions", db_file="tmp/storage.db")
)

# ============================================================================
# AGENTE FINANCEIRO
# ============================================================================
finance_agent = Agent(
    name="Finance_Analyst", 
    model=OpenAIChat(id="gpt-4.1-mini"),
    role="Especialista em análise financeira e investimentos",
    tools=[
        TavilyTools(search_depth="advanced", max_tokens=8000),
        XTools(wait_on_rate_limit=True, include_post_metrics=True),
        YFinanceTools(
            stock_price=True,
            company_info=True,
            stock_fundamentals=True,
            income_statements=True,
            key_financial_ratios=True,
            analyst_recommendations=True,
            company_news=True,
            technical_indicators=True,
            historical_prices=True
        ),
        YouTubeTools(),
        calculate_portfolio_metrics
    ],
    instructions=f"""
    {open("prompts/finance_agent.md").read()}
    
    IMPORTANTE: Hoje é {datetime.now().strftime('%d de %B de %Y')}.
    """,
    memory=memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=5,
    show_tool_calls=True,
    storage=SqliteStorage(table_name="finance_agent_sessions", db_file="tmp/storage.db")
)

# ============================================================================
# TIME DE AGENTES
# ============================================================================
intelligence_team = Team(
    name="Intelligence_Team",
    mode="route",  # Roteamento inteligente baseado na consulta
    model=OpenAIChat(id="gpt-4.1-mini"),
    members=[tech_ai_agent, finance_agent],
    instructions="""
    Você é o líder de uma equipe de especialistas em tecnologia e finanças. Sua função é:
    
    1. **ROTEAMENTO INTELIGENTE:**
       - Perguntas sobre programação, IA, frameworks → TechAI_Specialist
       - Perguntas sobre investimentos, ações, economia → Finance_Analyst
       - Perguntas mistas → Coordene ambos os agentes
    
    2. **CRITÉRIOS DE DECISÃO:**
       - Tecnologia: JavaScript, Python, IA, LLMs, frameworks, ferramentas dev
       - Finanças: Ações, investimentos, análise fundamentalista, criptomoedas
       - Ambos: Fintechs, startups de IA, empresas de tecnologia como investimento
    
    3. **QUANDO USAR AMBOS:**
       - Análise de empresas de tecnologia para investimento
       - Tendências que afetam tanto tech quanto mercado
       - Comparação entre empresas do setor tech
    
    Sempre identifique claramente qual especialista está respondendo.
    """,
    description="Equipe de especialistas em tecnologia/IA e análise financeira",
    memory=memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=10,
    show_tool_calls=True,
    show_members_responses=True,
    storage=SqliteStorage(table_name="team_sessions", db_file="tmp/storage.db"),
    markdown=True
)

# ============================================================================
# PLAYGROUND
# ============================================================================
playground = Playground(
    agents=[tech_ai_agent, finance_agent],
    teams=[intelligence_team]
)

app = playground.get_app()

if __name__ == "__main__":
    playground.serve(app="intelligence_team:app", reload=True, port=8888)
