"""
GitHub Drummer Animation Generator V2
Baterista GIF destruindo contribuições do GitHub quadradinho por quadradinho!
"""

import os
import sys
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests


class GitHubContributionFetcher:
    """Busca contribuições do GitHub via GraphQL API"""
    
    def __init__(self, username: str, token: str = None):
        self.username = username
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.api_url = 'https://api.github.com/graphql'
    
    def fetch_contributions(self):
        """Busca grid de contribuições dos últimos 365 dias"""
        query = """
        query($userName:String!) {
          user(login: $userName) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                  }
                }
              }
            }
          }
        }
        """
        
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        try:
            response = requests.post(
                self.api_url,
                json={'query': query, 'variables': {'userName': self.username}},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                print(f"API Error: {data['errors']}")
                return self._generate_mock_data()
            
            weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
            return self._process_weeks(weeks)
            
        except Exception as e:
            print(f"Failed to fetch contributions: {e}")
            print("Using mock data instead...")
            return self._generate_mock_data()
    
    def _process_weeks(self, weeks):
        """Processa semanas em grid"""
        grid = []
        for week in weeks:
            week_data = []
            for day in week['contributionDays']:
                week_data.append({
                    'count': day['contributionCount'],
                    'date': day['date']
                })
            grid.append(week_data)
        return grid
    
    def _generate_mock_data(self):
        """Gera dados mockados caso API falhe - igual ao visual real do GitHub"""
        import random
        grid = []
        for week in range(53):
            week_data = []
            for day in range(7):
                # 80% de chance de não ter contribuição (igual ao real)
                if random.random() < 0.80:
                    count = 0
                else:
                    count = random.randint(1, 10)
                
                week_data.append({
                    'count': count,
                    'date': '2024-01-01'
                })
            grid.append(week_data)
        return grid


class DrummerAnimationGenerator:
    """Gera SVG animado do baterista GIF destruindo contribuições"""
    
    def __init__(self, contribution_grid, assets_dir):
        self.grid = contribution_grid
        self.assets_dir = Path(assets_dir)
        # Dimensões iguais ao GitHub padrão (como na cobrinha)
        self.cell_size = 10
        self.cell_gap = 4
        self.drummer_gif_width = 120
        self.drummer_gif_height = 120
        
    def _encode_image_to_base64(self, image_path):
        """Converte imagem para base64 para embedar no SVG"""
        try:
            with open(image_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Warning: Could not encode {image_path}: {e}")
            return ""
    
    def _get_contribution_color(self, count):
        """Retorna cor baseada na quantidade de contribuições (tema GitHub escuro)"""
        if count == 0:
            return '#161b22'
        elif count < 3:
            return '#0e4429'
        elif count < 6:
            return '#006d32'
        elif count < 9:
            return '#26a641'
        else:
            return '#39d353'
    
    def generate_svg(self):
        """Gera o SVG completo com animação"""
        
        # Calcular dimensões
        grid_width = len(self.grid) * (self.cell_size + self.cell_gap)
        grid_height = 7 * (self.cell_size + self.cell_gap)
        total_width = max(self.drummer_gif_width, grid_width) + 60
        total_height = self.drummer_gif_height + grid_height + 80
        
        svg_parts = []
        
        # Header SVG
        svg_parts.append(f'''<svg width="{total_width}" height="{total_height}" 
            xmlns="http://www.w3.org/2000/svg" 
            xmlns:xlink="http://www.w3.org/1999/xlink">''')
        
        # Defs e Styles
        svg_parts.append(self._generate_defs_and_styles())
        
        # GIF do baterista (centralizado no topo)
        svg_parts.append(self._generate_drummer_gif())
        
        # Grid de contribuições (abaixo do GIF)
        svg_parts.append(self._generate_contribution_grid())
        
        # Efeitos de impacto
        svg_parts.append(self._generate_impact_effects())
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _generate_defs_and_styles(self):
        """Gera definições e estilos CSS"""
        return '''
        <defs>
            <!-- Filtro de brilho para efeito de impacto -->
            <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            
            <!-- Onda de choque -->
            <radialGradient id="shockwave">
                <stop offset="0%" style="stop-color:#ffd700;stop-opacity:0.8" />
                <stop offset="50%" style="stop-color:#ff6b6b;stop-opacity:0.4" />
                <stop offset="100%" style="stop-color:#4ecdc4;stop-opacity:0" />
            </radialGradient>
            
            <style>
                /* Animação do anel de impacto ao redor do GIF */
                @keyframes impact-ring {
                    0%, 100% { 
                        transform: scale(0.8);
                        opacity: 0;
                    }
                    50% { 
                        transform: scale(1.5);
                        opacity: 0.6;
                    }
                }
                
                /* Animação igual à cobrinha - célula só some no lugar */
                @keyframes cell-explode {
                    0% {
                        opacity: 1;
                    }
                    100% {
                        opacity: 0;
                    }
                }
                
                /* Pulso no baterista nas batidas */
                @keyframes drummer-pulse {
                    0%, 90%, 100% {
                        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
                    }
                    95% {
                        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.6)) drop-shadow(0 4px 8px rgba(0,0,0,0.4));
                    }
                }
                
                .drummer-container {
                    animation: drummer-pulse 0.15s ease-out infinite;
                }
                
                .impact-ring {
                    animation: impact-ring 0.15s ease-out infinite;
                }
                
                .cell {
                    animation: cell-explode 0.2s ease-out forwards;
                }
            </style>
        </defs>
        '''
    
    def _generate_drummer_gif(self):
        """Gera o GIF do baterista centralizado no topo"""
        parts = []
        
        # Calcular largura real do grid
        grid_width = len(self.grid) * (self.cell_size + self.cell_gap) - self.cell_gap
        
        # Centralizar GIF perfeitamente em relação ao grid
        # Grid começa em x=30, então GIF deve estar centralizado nessa mesma área
        x_center = 30 + (grid_width - self.drummer_gif_width) / 2
        
        # Embedar GIF
        gif_path = self.assets_dir / 'drum.gif'
        gif_base64 = self._encode_image_to_base64(gif_path)
        
        parts.append(f'<g class="drummer-container" transform="translate({x_center}, 20)">')
        
        # Anéis de impacto (aparecem no ritmo das batidas)
        for i in range(3):
            delay = i * 0.05
            parts.append(f'''
                <circle class="impact-ring" 
                    cx="{self.drummer_gif_width/2}" 
                    cy="{self.drummer_gif_height/2}" 
                    r="50" 
                    fill="none" 
                    stroke="url(#shockwave)" 
                    stroke-width="2"
                    style="animation-delay: {delay}s;"
                    opacity="0"/>
            ''')
        
        # GIF do baterista
        if gif_base64:
            parts.append(f'''
                <image 
                    href="data:image/gif;base64,{gif_base64}"
                    width="{self.drummer_gif_width}" 
                    height="{self.drummer_gif_height}"
                    style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));"
                />
            ''')
        else:
            # Fallback se GIF não carregar
            parts.append(f'''
                <rect 
                    width="{self.drummer_gif_width}" 
                    height="{self.drummer_gif_height}" 
                    rx="10"
                    fill="#7aa2f7"
                    opacity="0.3"/>
                <text 
                    x="{self.drummer_gif_width/2}" 
                    y="{self.drummer_gif_height/2}" 
                    text-anchor="middle" 
                    dominant-baseline="middle"
                    fill="white" 
                    font-size="60">🥁</text>
            ''')
        
        parts.append('</g>')
        
        return '\n'.join(parts)
    
    def _generate_contribution_grid(self):
        """Gera grid de contribuições com efeito de explosão sequencial APENAS em células com contribuição"""
        parts = []
        
        # Grid fixo com offset de 30px (igual ao GIF)
        x_offset = 30
        y_offset = self.drummer_gif_height + 40  # Mais próximo do GIF
        
        parts.append(f'<g id="contribution-grid" transform="translate({x_offset}, {y_offset})">')
        
        # Primeiro, coletar apenas células com contribuição
        cells_with_contribution = []
        all_cells = []
        
        for week_idx, week in enumerate(self.grid):
            for day_idx, day in enumerate(week):
                x = week_idx * (self.cell_size + self.cell_gap)
                y = day_idx * (self.cell_size + self.cell_gap)
                color = self._get_contribution_color(day['count'])
                
                cell_data = {
                    'x': x,
                    'y': y,
                    'color': color,
                    'count': day['count']
                }
                all_cells.append(cell_data)
                
                if day['count'] > 0:
                    cells_with_contribution.append(cell_data)
        
        # Timing: uma célula COM contribuição explode a cada 0.15s
        cell_delay = 0.15  # segundos entre cada explosão
        total_duration = len(cells_with_contribution) * cell_delay
        
        # Criar lookup de delays
        contribution_cells_lookup = {id(cell): idx for idx, cell in enumerate(cells_with_contribution)}
        
        # Renderizar TODAS as células, mas só animar as que têm contribuição
        for cell in all_cells:
            x = cell['x']
            y = cell['y']
            color = cell['color']
            count = cell['count']
            
            if count > 0:
                # Célula COM contribuição - EXPLODE no lugar!
                cell_id = id(cell)
                if cell_id in contribution_cells_lookup:
                    explosion_index = contribution_cells_lookup[cell_id]
                    delay = explosion_index * cell_delay
                    
                    # Só a célula, sem partículas (clean)
                    parts.append(f'''
                        <rect class="cell" 
                            x="{x}" y="{y}" 
                            width="{self.cell_size}" 
                            height="{self.cell_size}" 
                            rx="2"
                            fill="{color}"
                            style="animation-delay: {delay}s; 
                                   animation-iteration-count: infinite; 
                                   animation-duration: {total_duration}s;">
                        </rect>
                    ''')
            else:
                # Célula SEM contribuição - fica ESTÁTICA
                parts.append(f'''
                    <rect 
                        x="{x}" y="{y}" 
                        width="{self.cell_size}" 
                        height="{self.cell_size}" 
                        rx="2"
                        fill="{color}">
                    </rect>
                ''')
        
        parts.append('</g>')
        return '\n'.join(parts)
    
    def _generate_impact_effects(self):
        """Sem efeitos extras - visual limpo"""
        return ''


def main():
    """Função principal"""
    print("GitHub Drummer Animation Generator V2")
    print("=" * 50)
    
    # Configurações
    username = os.environ.get('GITHUB_USERNAME', 'henrilouc')
    github_token = os.environ.get('GITHUB_TOKEN')
    
    # Diretórios
    script_dir = Path(__file__).parent
    assets_dir = script_dir.parent / 'assets'
    output_file = assets_dir / 'drummer-animation.svg'
    
    # Verificar se GIF existe
    gif_file = assets_dir / 'drum.gif'
    if not gif_file.exists():
        print(f"ERROR: drum.gif not found in {assets_dir}")
        print("Please add your drum.gif file to the assets folder!")
        sys.exit(1)
    
    # Criar pasta assets se não existir
    assets_dir.mkdir(exist_ok=True)
    
    print(f"Fetching contributions for @{username}...")
    fetcher = GitHubContributionFetcher(username, github_token)
    contributions = fetcher.fetch_contributions()
    
    print(f"Got {len(contributions)} weeks of data")
    print(f"Generating SVG animation...")
    
    generator = DrummerAnimationGenerator(contributions, assets_dir)
    svg_content = generator.generate_svg()
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Animation generated successfully!")
    print(f"Output: {output_file}")
    print("\nAnimation features:")
    print("- Drummer GIF with pulsing impact effect")
    print("- Contribution cells exploding one by one")
    print("- Particles flying on each explosion")
    print("- Synchronized with drum beats (0.15s interval)")
    print("\nRun this daily with GitHub Actions to keep it updated!")


if __name__ == '__main__':
    main()
