#!/usr/bin/env python3
import os
import re
import requests

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = 'warasugitewara'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_user_stats():
    """Get user stats from GitHub API"""
    url = f'https://api.github.com/users/{USERNAME}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    return {
        'public_repos': data['public_repos'],
        'followers': data['followers'],
        'following': data['following']
    }

def get_top_languages():
    """Get top languages from user repos"""
    url = f'https://api.github.com/users/{USERNAME}/repos?per_page=100'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
    
    repos = response.json()
    languages = {}
    
    for repo in repos:
        if repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    
    # Top 4 languages by repo count
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:4]
    return [lang[0] for lang in top_langs]

def update_readme(stats, languages):
    """Update README with new stats"""
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update stats badges
    public_repos = stats['public_repos']
    followers = stats['followers']
    following = stats['following']
    
    # Create new stats section
    new_stats = f"""<h2 align="center">📊 My Stats.</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Public%20Repositories-{public_repos}-blue?style=flat-square" alt="Repos" />
  <img src="https://img.shields.io/badge/Followers-{followers}-green?style=flat-square" alt="Followers" />
  <img src="https://img.shields.io/badge/Following-{following}-orange?style=flat-square" alt="Following" />
</p>

<p align="center">
  <strong>🔝 Top Languages:</strong><br>
  {' • '.join(languages)}
</p>"""
    
    # Replace the stats section
    pattern = r'<h2 align="center">📊 My Stats\.</h2>.*?(?=<h2 align="center">🎮|$)'
    new_content = re.sub(pattern, new_stats + '\n\n', content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ README updated!")
    print(f"   Public Repos: {public_repos}")
    print(f"   Followers: {followers}")
    print(f"   Following: {following}")
    print(f"   Top Languages: {', '.join(languages)}")

if __name__ == '__main__':
    print("🔄 Fetching GitHub stats...")
    stats = get_user_stats()
    
    if not stats:
        print("❌ Failed to fetch stats")
        exit(1)
    
    print("🔍 Analyzing repositories...")
    languages = get_top_languages()
    
    print("📝 Updating README...")
    update_readme(stats, languages)
    print("✅ Done!")
