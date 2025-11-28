#!/usr/bin/env python3
"""
Generate HTML visualization files for each MLB prospect release.
Creates scatter plots showing Career WAR vs Career Length for each release.
"""

import json
import os
from pathlib import Path

def load_data(json_path):
    """Load the MLB analysis results JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def filter_players(players):
    """Filter players to only include those who debuted and have WAR > 0."""
    filtered = []
    for player in players:
        # Check if player debuted (debut is not None/NaN) and has positive WAR
        if (player.get('debut') is not None and 
            not (isinstance(player.get('debut'), float) and str(player.get('debut')).lower() == 'nan') and
            player.get('war') is not None and
            not (isinstance(player.get('war'), float) and str(player.get('war')).lower() == 'nan') and
            player.get('war', 0) > 0):
            filtered.append(player)
    return filtered

def generate_release_html(release_data, all_releases):
    """Generate HTML file for a single release."""
    release_name = release_data['release']
    players = filter_players(release_data.get('players', []))
    
    if not players:
        return None  # Skip releases with no valid players
    
    # Prepare data for plotting
    player_names = [p['name'] for p in players]
    war_values = [p['war'] for p in players]
    career_lengths = [p['career_length'] for p in players]
    
    # Create HTML with embedded Plotly
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{release_name} - Prospect Visualization</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}
        #plot {{
            width: 100%;
            height: 600px;
        }}
        .stats {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }}
        .stats p {{
            margin: 5px 0;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{release_name}</h1>
        <p class="subtitle">Career WAR vs Career Length</p>
        <div id="plot"></div>
        <div class="stats">
            <p><strong>Total Players Shown:</strong> {len(players)}</p>
            <p><strong>Average WAR:</strong> {sum(war_values) / len(war_values):.2f}</p>
            <p><strong>Average Career Length:</strong> {sum(career_lengths) / len(career_lengths):.2f} years</p>
        </div>
    </div>

    <script>
        var data = [{{
            x: {war_values},
            y: {career_lengths},
            mode: 'markers+text',
            type: 'scatter',
            text: {json.dumps(player_names)},
            textposition: 'top center',
            textfont: {{
                size: 10,
                color: '#333'
            }},
            marker: {{
                size: 8,
                color: '#1f77b4',
                opacity: 0.7,
                line: {{
                    width: 1,
                    color: '#fff'
                }}
            }},
            hovertemplate: '<b>%{{text}}</b><br>' +
                          'Career WAR: %{{x}}<br>' +
                          'Career Length: %{{y}} years<extra></extra>'
        }}];

        var layout = {{
            title: {{
                text: '{release_name} - Career WAR vs Career Length',
                font: {{ size: 18 }}
            }},
            xaxis: {{
                title: 'Career WAR',
                titlefont: {{ size: 14 }},
                showgrid: true,
                gridcolor: '#e0e0e0'
            }},
            yaxis: {{
                title: 'Career Length (years)',
                titlefont: {{ size: 14 }},
                showgrid: true,
                gridcolor: '#e0e0e0'
            }},
            plot_bgcolor: 'white',
            paper_bgcolor: 'white',
            hovermode: 'closest'
        }};

        var config = {{
            responsive: true,
            displayModeBar: true
        }};

        Plotly.newPlot('plot', data, layout, config);
    </script>
</body>
</html>
"""
    
    return html_content

def generate_index_html(all_releases):
    """Generate main index.html with tabs for all releases."""
    # Filter releases to only include those with valid players
    valid_releases = []
    for release in all_releases:
        players = filter_players(release.get('players', []))
        if players:
            valid_releases.append({
                'name': release['release'],
                'year': release.get('year', 0),
                'set': release.get('set', ''),
                'player_count': len(players)
            })
    
    # Sort by year, then by set name
    valid_releases.sort(key=lambda x: (x['year'], x['set']))
    
    # Generate tab HTML
    tabs_html = ''
    tab_content_html = ''
    
    for i, release in enumerate(valid_releases):
        release_name = release['name']
        filename = release_name.lower().replace(' ', '_').replace('&', 'and') + '.html'
        active_class = 'active' if i == 0 else ''
        show_class = 'show active' if i == 0 else ''
        
        tabs_html += f'''
        <li class="nav-item">
            <a class="nav-link {active_class}" id="{filename}-tab" data-bs-toggle="tab" href="#{filename}" role="tab" aria-controls="{filename}">
                {release_name}
            </a>
        </li>'''
        
        tab_content_html += f'''
        <div class="tab-pane fade {show_class}" id="{filename}" role="tabpanel">
            <iframe src="{filename}" style="width: 100%; height: 800px; border: none;"></iframe>
        </div>'''
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MLB Prospect Success Rate Visualizations</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .nav-tabs {{
            border-bottom: 2px solid #dee2e6;
            padding: 0 20px;
            background-color: #f8f9fa;
        }}
        .nav-tabs .nav-link {{
            color: #495057;
            border: none;
            border-bottom: 3px solid transparent;
            padding: 15px 20px;
        }}
        .nav-tabs .nav-link:hover {{
            border-bottom-color: #667eea;
            color: #667eea;
        }}
        .nav-tabs .nav-link.active {{
            color: #667eea;
            background-color: white;
            border-bottom-color: #667eea;
            font-weight: 600;
        }}
        .tab-content {{
            padding: 0;
        }}
        .stats-summary {{
            padding: 20px;
            background-color: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }}
        .stats-summary p {{
            margin: 5px 0;
            color: #495057;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>MLB Prospect Success Rate Analysis</h1>
            <p>Interactive visualizations showing Career WAR vs Career Length for each release</p>
        </div>
        <ul class="nav nav-tabs" id="releaseTabs" role="tablist">
            {tabs_html}
        </ul>
        <div class="tab-content" id="releaseTabContent">
            {tab_content_html}
        </div>
        <div class="stats-summary">
            <p><strong>Total Releases:</strong> {len(valid_releases)}</p>
            <p><strong>Note:</strong> Only players who debuted with WAR > 0 are displayed</p>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Enable Bootstrap tabs
        var triggerTabList = [].slice.call(document.querySelectorAll('#releaseTabs a'));
        triggerTabList.forEach(function (triggerEl) {{
            var tabTrigger = new bootstrap.Tab(triggerEl);
            triggerEl.addEventListener('click', function (event) {{
                event.preventDefault();
                tabTrigger.show();
            }});
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    """Main function to generate all HTML files."""
    # Paths
    script_dir = Path(__file__).parent
    data_path = Path('/Users/andrewdahl/Downloads/mlb_analysis_results.json')
    output_dir = script_dir
    
    # Load data
    print("Loading data...")
    data = load_data(data_path)
    all_releases = data.get('all_releases', [])
    
    print(f"Found {len(all_releases)} releases")
    
    # Generate individual release HTML files
    print("Generating individual release HTML files...")
    generated_files = []
    for release in all_releases:
        html_content = generate_release_html(release, all_releases)
        if html_content:
            release_name = release['release']
            filename = release_name.lower().replace(' ', '_').replace('&', 'and') + '.html'
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            generated_files.append(filename)
            print(f"  Generated: {filename}")
    
    # Generate index.html
    print("Generating index.html...")
    index_html = generate_index_html(all_releases)
    index_path = output_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  Generated: index.html")
    
    print(f"\nDone! Generated {len(generated_files)} release files and index.html")
    print(f"Total files: {len(generated_files) + 1}")

if __name__ == '__main__':
    main()

