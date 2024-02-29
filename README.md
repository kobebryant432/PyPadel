# PyPadel

PyPadel is a comprehensive tool designed for generating detailed statistics for padel matches. It allows users to input match data, analyze it, and export the results for further use. Whether you're a coach, player, or enthusiast, PyPadel offers valuable insights into match dynamics and player performance.

## Features

- **Match Analysis**: Generate detailed statistics from padel matches, including point-by-point breakdowns, serve efficiency, and more.
- **Database Integration**: Easily manage match data using SQLite databases. Import from or export to Excel files for convenient data handling.
- **Statistical Insights**: Access a variety of statistical analyses, from basic match summaries to advanced metrics like golden points and break point conversions.

## Getting Started

### Prerequisites

Ensure you have Python 3.10 or later installed on your system. Dependencies include pandas for data manipulation and SQLite for database management.

   ```
   pip install -r requirements.txt
   ```

### Usage

For comprehensive usage examples, including match handling and database management, refer to `example.py` and `db_tutorial.ipynb` respectively. Below are some basic operations to get you started:

1. **Initializing the Database**:
   To initialize or load an existing database for storing match data, use:
   ```python
    from database import SqlDatabase
    # This either opens an existing database or creates a new one
    db_tutorial = SqlDatabase(name="test")
    db_tutorial.load_db(file=xlsx_path/"local_inputs.csv")

    db = SqlDatabase.init_from_existing(db_filename="path/to/padel_matches.db")
   ```

2. **Adding Match Data**:
   You can input match details either manually or by importing them from an Excel file:
   ```python
   m = start_match()
   db.add_match(m=m)
   ```

3. **Generating Statistics**:
   To access detailed statistics of matches and export them for further analysis:
   ```python
   match_stats = db.get_match_stats(match_id=21)
   print(match_stats)
   ```

4. **Exporting Data**:
   For exporting the database content to Excel or as raw data:
   ```python
   db.export_all()
   ```

## Contributing

Contributions to PyPadel are welcome! Whether it's bug reports, feature requests, or code contributions, feel free to open an issue or submit a pull request.

## License

PyPadel is open-source software licensed under the MIT license.