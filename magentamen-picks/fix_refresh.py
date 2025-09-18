# Script to fix the refresh function to always fetch fresh data
import re

# Read the current app.py file
with open('app.py', 'r') as f:
    content = f.read()

# Find the refresh function and replace the stored results logic
old_logic = '''        # First, check if we already have stored game results
        stored_results = GameResult.query.filter_by(week=week, season=season, final=True).all()
        
        if stored_results:
            # Use stored results instead of fetching from API
            print(f"Using {len(stored_results)} stored game results for Week {week}")
            game_results = {}
            
            for result in stored_results:
                game_key = f"{result.away_team} @ {result.home_team}"
                game_results[game_key] = {
                    "home_score": result.home_score,
                    "away_score": result.away_score,
                    "final": result.final,
                    "spread": result.spread,
                    "total": result.total,
                    "moneyline_winner": result.moneyline_winner,
                    "spread_winner": result.spread_winner,
                    "total_result": result.total_result
                }
        else:
            # Fetch fresh results from API
            game_results = fetch_game_results(week, season)
            
            if not game_results:
                return jsonify({
                    'success': False,
                    'message': f'No completed games found for Week {week}. Games may not have been played yet.'
                }), 400
            
            # Store results in database
            stored_count = store_game_results(week, season, game_results)'''

new_logic = '''        # Always fetch fresh results from API using daysFrom=3
        print(f"=== FETCHING FRESH DATA FOR WEEK {week} ===")
        game_results = fetch_game_results(week, season)
        
        if not game_results:
            return jsonify({
                'success': False,
                'message': f'No completed games found for Week {week}. Games may not have been played yet.'
            }), 400
        
        # Store results in database
        stored_count = store_game_results(week, season, game_results)'''

# Replace the logic
new_content = content.replace(old_logic, new_logic)

# Also need to update the return statement
old_return = '''        if stored_results:
            return jsonify({
                'success': True,
                'message': f'Used stored game results and updated {results_updated} pick outcomes for Week {week}',
                'games_updated': len(stored_results),
                'picks_updated': results_updated
            })
        else:
            return jsonify({
                'success': True,
                'message': f'Refreshed {stored_count} game results and updated {results_updated} pick outcomes for Week {week}',
                'games_updated': stored_count,
                'picks_updated': results_updated
            })'''

new_return = '''        return jsonify({
            'success': True,
            'message': f'Fetched fresh data and updated {results_updated} pick outcomes for Week {week}',
            'games_updated': stored_count,
            'picks_updated': results_updated
        })'''

new_content = new_content.replace(old_return, new_return)

# Write the updated content
with open('app.py', 'w') as f:
    f.write(new_content)

print("Successfully updated refresh function to always fetch fresh data!")
