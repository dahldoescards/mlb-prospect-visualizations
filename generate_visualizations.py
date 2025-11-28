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
    avg_war = sum(war_values) / len(war_values) if war_values else 0
    avg_career = sum(career_lengths) / len(career_lengths) if career_lengths else 0
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{release_name} | Bowman Prospect Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 30px;
        }}
        .header-section {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }}
        h1 {{
            color: #1e3c72;
            margin: 0 0 8px 0;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}
        .subtitle {{
            color: #6c757d;
            margin: 0;
            font-size: 1rem;
            font-weight: 400;
        }}
        #plot {{
            width: 100%;
            height: 650px;
            margin: 30px 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-label {{
            display: block;
            font-size: 0.85rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .stat-value {{
            display: block;
            font-size: 1.75rem;
            color: #1e3c72;
            font-weight: 700;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 20px 15px;
            }}
            h1 {{
                font-size: 1.5rem;
            }}
            #plot {{
                height: 500px;
            }}
            .stats {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>{release_name}</h1>
            <p class="subtitle">Career WAR vs Career Length Analysis</p>
        </div>
        <div id="plot"></div>
        <div class="stats">
            <div class="stat-item">
                <span class="stat-label">Players Shown</span>
                <span class="stat-value">{len(players)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Average WAR</span>
                <span class="stat-value">{avg_war:.2f}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Avg Career Length</span>
                <span class="stat-value">{avg_career:.1f} yrs</span>
            </div>
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
                size: 10,
                color: '#2a5298',
                opacity: 0.8,
                line: {{
                    width: 2,
                    color: '#ffffff'
                }}
            }},
            hovertemplate: '<b>%{{text}}</b><br>' +
                          'Career WAR: %{{x}}<br>' +
                          'Career Length: %{{y}} years<extra></extra>'
        }}];

        var layout = {{
            title: {{
                text: '',
                font: {{ size: 0 }}
            }},
            xaxis: {{
                title: {{
                    text: 'Career WAR',
                    font: {{ size: 16, family: 'Inter, sans-serif', color: '#1e3c72' }}
                }},
                titlefont: {{ size: 16, family: 'Inter, sans-serif' }},
                showgrid: true,
                gridcolor: '#e9ecef',
                gridwidth: 1,
                zeroline: false,
                linecolor: '#dee2e6',
                linewidth: 1
            }},
            yaxis: {{
                title: {{
                    text: 'Career Length (years)',
                    font: {{ size: 16, family: 'Inter, sans-serif', color: '#1e3c72' }}
                }},
                titlefont: {{ size: 16, family: 'Inter, sans-serif' }},
                showgrid: true,
                gridcolor: '#e9ecef',
                gridwidth: 1,
                zeroline: false,
                linecolor: '#dee2e6',
                linewidth: 1
            }},
            plot_bgcolor: '#ffffff',
            paper_bgcolor: '#ffffff',
            hovermode: 'closest',
            margin: {{
                l: 80,
                r: 40,
                t: 20,
                b: 60
            }},
            font: {{
                family: 'Inter, sans-serif',
                size: 12,
                color: '#495057'
            }}
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
    """Generate main index.html with dropdown menu for all releases."""
    # Filter releases to only include those with valid players
    valid_releases = []
    for release in all_releases:
        players = filter_players(release.get('players', []))
        if players:
            valid_releases.append({
                'name': release['release'],
                'year': release.get('year', 0),
                'set': release.get('set', ''),
                'player_count': len(players),
                'filename': release['release'].lower().replace(' ', '_').replace('&', 'and') + '.html'
            })
    
    # Sort by year (descending), then by set name
    valid_releases.sort(key=lambda x: (-x['year'], x['set']))
    
    # Generate dropdown options
    dropdown_options = ''
    for release in valid_releases:
        dropdown_options += f'<option value="{release["filename"]}">{release["name"]}</option>\n'
    
    # Get first release for initial display
    first_release = valid_releases[0] if valid_releases else None
    
    initial_file = first_release['filename'] if first_release else ''
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bowman Prospect Analysis | Career WAR Visualizations</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 0;
            margin: 0;
        }}
        .main-container {{
            max-width: 1600px;
            margin: 40px auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 50px 40px;
            border-bottom: 4px solid #ffd700;
        }}
        .header h1 {{
            margin: 0 0 12px 0;
            font-size: 2.75rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .header .subtitle {{
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.95;
            font-weight: 400;
        }}
        .controls-section {{
            padding: 30px 40px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        .release-selector {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .release-selector label {{
            font-weight: 600;
            color: #495057;
            margin: 0;
            font-size: 1rem;
        }}
        .release-selector select {{
            flex: 1;
            max-width: 500px;
            padding: 12px 16px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            background-color: white;
            color: #212529;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .release-selector select:hover {{
            border-color: #2a5298;
        }}
        .release-selector select:focus {{
            outline: none;
            border-color: #2a5298;
            box-shadow: 0 0 0 3px rgba(42, 82, 152, 0.1);
        }}
        .visualization-container {{
            position: relative;
            min-height: 700px;
            background-color: #ffffff;
        }}
        .visualization-container iframe {{
            width: 100%;
            height: 800px;
            border: none;
            display: block;
        }}
        .stats-summary {{
            padding: 25px 40px;
            background: linear-gradient(to right, #f8f9fa, #ffffff);
            border-top: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .stats-summary .stat-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .stats-summary .stat-label {{
            font-weight: 600;
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .stats-summary .stat-value {{
            font-weight: 700;
            color: #2a5298;
            font-size: 1.1rem;
        }}
        .stats-summary .note {{
            color: #6c757d;
            font-size: 0.9rem;
            font-style: italic;
        }}
        @media (max-width: 768px) {{
            .main-container {{
                margin: 20px;
                border-radius: 8px;
            }}
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 2rem;
            }}
            .controls-section {{
                padding: 20px;
            }}
            .release-selector {{
                flex-direction: column;
                align-items: stretch;
            }}
            .release-selector select {{
                max-width: 100%;
            }}
            .stats-summary {{
                padding: 20px;
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>Bowman Prospect Analysis</h1>
            <p class="subtitle">Career WAR vs Career Length Visualizations</p>
        </div>
        <div class="controls-section">
            <div class="release-selector">
                <label for="releaseSelect">Select Release:</label>
                <select id="releaseSelect" class="form-select">
                    {dropdown_options}
                </select>
            </div>
        </div>
        <div class="visualization-container">
            <iframe id="visualizationFrame" src="{initial_file}" style="width: 100%; height: 800px; border: none;"></iframe>
        </div>
        <div class="stats-summary">
            <div class="stat-item">
                <span class="stat-label">Total Releases:</span>
                <span class="stat-value">{len(valid_releases)}</span>
            </div>
            <div class="note">Only players who debuted with WAR > 0 are displayed</div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('releaseSelect').addEventListener('change', function(e) {{
            const selectedFile = e.target.value;
            document.getElementById('visualizationFrame').src = selectedFile;
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

