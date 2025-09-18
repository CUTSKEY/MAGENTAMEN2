def fetch_game_results(week, season):
    """
    Fetch live game results from The Odds API scores endpoint using daysFrom=3
    """
    if not ODDS_API_KEY:
        print("No API key available for fetching game results")
        return {}
    
    try:
        # Use daysFrom=3 to get games from the last 3 days
        scores_url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/scores/'
        params = {
            'apiKey': ODDS_API_KEY,
            'dateFormat': 'iso',
            'daysFrom': 3  # Get games from last 3 days
        }
        
        print(f"Fetching games from last 3 days...")
        
        response = requests.get(scores_url, params=params)
        response.raise_for_status()
        
        scores_data = response.json()
        
        print(f"API returned {len(scores_data)} total games")
        
        # Get already stored completed games to avoid re-processing
        stored_games = set()
        existing_results = GameResult.query.filter_by(final=True).all()
        for result in existing_results:
            game_key = f"{result.away_team} @ {result.home_team}"
            stored_games.add(game_key)
        
        print(f"Already have {len(stored_games)} completed games stored")
        
        # Process the scores data
        game_results = {}
        completed_games = 0
        total_games = len(scores_data)
        
        for game in scores_data:
            if game.get('completed') and game.get('scores'):
                home_team = game['home_team']
                away_team = game['away_team']
                game_key = f"{away_team} @ {home_team}"
                
                # Skip if we already have this completed game
                if game_key in stored_games:
                    print(f"Skipping already stored game: {game_key}")
                    continue
                
                completed_games += 1
                
                # Extract scores
                home_score = None
                away_score = None
                for score in game['scores']:
                    if score['name'] == home_team:
                        home_score = score['score']
                    elif score['name'] == away_team:
                        away_score = score['score']
                
                if home_score is not None and away_score is not None:
                    # Determine moneyline winner
                    if home_score > away_score:
                        moneyline_winner = home_team
                    elif away_score > home_score:
                        moneyline_winner = away_team
                    else:
                        moneyline_winner = None  # Tie
                    
                    # Get spread and total from stored odds data
                    spread_winner = None
                    total_result = None
                    spread = None
                    total = None
                    
                    # Find the corresponding game in our database to get odds
                    db_game = Game.query.filter_by(
                        week=week,
                        season=season,
                        home_team=home_team,
                        away_team=away_team
                    ).first()
                    
                    if db_game and db_game.odds_data:
                        try:
                            odds_data = json.loads(db_game.odds_data)
                            # Find DraftKings odds
                            draftkings = None
                            for bookmaker in odds_data:
                                if bookmaker.get('key') == 'draftkings':
                                    draftkings = bookmaker
                                    break
                            
                            if draftkings and draftkings.get('markets'):
                                # Get spread data
                                spreads_market = None
                                for market in draftkings['markets']:
                                    if market.get('key') == 'spreads':
                                        spreads_market = market
                                        break
                                
                                if spreads_market and spreads_market.get('outcomes'):
                                    for outcome in spreads_market['outcomes']:
                                        if outcome['name'] == home_team:
                                            spread = outcome['point']
                                            break
                                
                                # Get total data
                                totals_market = None
                                for market in draftkings['markets']:
                                    if market.get('key') == 'totals':
                                        totals_market = market
                                        break
                                
                                if totals_market and totals_market.get('outcomes'):
                                    for outcome in totals_market['outcomes']:
                                        if outcome['name'] == 'Over':
                                            total = outcome['point']
                                            break
                                
                                # Calculate spread winner
                                if spread is not None:
                                    home_with_spread = home_score + spread
                                    if home_with_spread > away_score:
                                        spread_winner = home_team
                                    elif away_score > home_with_spread:
                                        spread_winner = away_team
                                    # else it's a push (tie)
                                
                                # Calculate total result
                                if total is not None:
                                    total_points = home_score + away_score
                                    if total_points > total:
                                        total_result = "over"
                                    elif total_points < total:
                                        total_result = "under"
                                    # else it's a push
                                        
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error parsing odds data for {game_key}: {e}")
                    
                    game_results[game_key] = {
                        "home_score": home_score,
                        "away_score": away_score,
                        "final": True,
                        "spread": spread,
                        "total": total,
                        "moneyline_winner": moneyline_winner,
                        "spread_winner": spread_winner,
                        "total_result": total_result
                    }
                    
                    print(f"Processed new completed game: {game_key} - {away_score}-{home_score}")
        
        print(f"Found {completed_games} NEW completed games out of {total_games} total games")
        print(f"Stored {len(stored_games)} games already in database")
        return game_results
        
    except requests.RequestException as e:
        print(f"Error fetching game results from API: {e}")
        return {}
    except Exception as e:
        print(f"Error processing game results: {e}")
        return {}
