# Testing Directory for Magentamen Picks

This directory contains test scripts to verify the functionality of the Magentamen Picks application.

## Test Files

### `test_database.py`
Tests the database structure and sample data. This test:
- Verifies all database tables have data
- Shows sample data from each table
- Displays data quality metrics
- **Can be run independently** (doesn't require Flask app)

### `test_backend.py`
Tests the Flask API endpoints. This test:
- Tests all major API endpoints
- Verifies data retrieval and updates
- Tests picks functionality
- Tests game results and week locking
- **Requires Flask app to be running** (`python app.py`)

### `simulate_weeks.py`
Simulates realistic game results for testing. This script:
- Generates realistic NFL scores for weeks 1-4
- Calculates pick outcomes based on simulated results
- Updates the database with simulated data
- **Can be run independently** (doesn't require Flask app)

### `run_tests.py`
A test runner that executes all tests and provides a summary.

## How to Run Tests

### Option 1: Run Individual Tests
```bash
cd testing
python test_database.py      # Test database structure
python test_backend.py       # Test API endpoints (requires Flask app)
python simulate_weeks.py     # Simulate game results
```

### Option 2: Run All Tests
```bash
cd testing
python run_tests.py
```

### Option 3: Run Backend Tests with Flask App
```bash
# Terminal 1: Start Flask app
cd ..  # Go back to main directory
python app.py

# Terminal 2: Run backend tests
cd testing
python test_backend.py
```

## Troubleshooting

### Import Error: "No module named 'app'"
This happens when running tests from the `testing/` directory. The fix has been applied to all test files - they now automatically add the parent directory to the Python path.

### Flask App Not Running
The `test_backend.py` requires the Flask app to be running. Start it with:
```bash
cd ..  # Go back to main directory
python app.py
```

### Database Issues
If you get database errors, make sure:
1. The database file exists (`instance/picks.db`)
2. You have the required dependencies installed (`pip install -r requirements.txt`)
3. The database has been initialized with sample data

## Test Results

When tests run successfully, you should see:
- ✅ Database test: Shows data structure and sample data
- ✅ Backend test: Tests API endpoints (if Flask app is running)
- ✅ Simulation: Generates realistic game results for testing

The tests will help you verify that:
- Database structure is correct
- Sample data is loaded properly
- API endpoints work as expected
- Game simulation produces realistic results
