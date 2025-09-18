from app import app, db, Game, GameResult
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    print("=== DEBUGGING GAME MATCHING LOGIC ===")
    
    # Get completed games from API
    api_key = os.getenv('ODDS_API_KEY')
    scores_url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/scores/'
    params = {
        'apiKey': api_key,
        'dateFormat': 'iso',
        'daysFrom': 3
    }
    
    response = requests.get(scores_url, params=params)
    scores_data = response.json()
    
    completed_games = [game for game in scores_data if game.get('completed') and game.get('scores')]
    print(f"API returned {len(completed_games)} completed games")
    
    # Get Week 2 games from our database
    week2_games = Game.query.filter_by(week=2, season=2025).all()
    print(f"Our database has {len(week2_games)} games for Week 2")
    
    # Check matching
    print("\n=== GAME MATCHING ANALYSIS ===")
    for api_game in completed_games:
        home_team = api_game['home_team']
        away_team = api_game['away_team']
        game_key = f"{away_team} @ {home_team}"
        
        print(f"\nAPI Game: {game_key}")
        
        # Check if this game exists in our Week 2 database
        db_game = Game.query.filter_by(
            week=2,
            season=2025,
            home_team=home_team,
            away_team=away_team
        ).first()
        
        if db_game:
            print(f"  ✅ Found in Week 2 database")
        else:
            print(f"  ❌ NOT found in Week 2 database")
            # Check if it exists in any week
            any_game = Game.query.filter_by(
                season=2025,
                home_team=home_team,
                away_team=away_team
            ).first()
            if any_game:
                print(f"  📍 Found in Week {any_game.week} instead")
            else:
                print(f"  ❌ Not found in any week")
