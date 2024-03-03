# PyPadel

PyPadel is a comprehensive tool designed for generating detailed statistics for padel matches. It allows users to input match data, analyze it, and export the results for further use. Whether you're a coach, player, or enthusiast, PyPadel offers valuable insights into match dynamics and player performance.

## Features

- **Match Analysis**: Generate detailed statistics from padel matches, including point-by-point breakdowns, serve efficiency, and more.
- **Database Integration**: Easily manage match data using SQLite databases. Import from or export to Excel files for convenient data handling.
- **Statistical Insights**: Access a variety of statistical analyses, from basic match summaries to advanced metrics like golden points and break point conversions.

## Getting Started

PyPadel represents padel matches through a unique encoding system that uses a sequence of letters to denote the events of each point in a match. This method allows for an efficient and compact representation of match data, making it easier for the computer to process and analyze the game's dynamics.

Each letter in the sequence corresponds to a specific event or outcome of a point, such as a serve, fault, winner, or unforced error. By reading and interpreting this string of letters, PyPadel can reconstruct the flow of the match and generate detailed statistics that provide insights into player performance and match strategy.

This approach simplifies the storage and processing of match data, enabling quick and comprehensive analysis of padel matches.

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

### Basic Concepts: User Input Manual

An example of a possible input in PyPadel is “e1ufhvn”, this is the input for the following point: The point started with a first serve (e) and the last shot of the point was played by player 1 (1). The shot player 1 hit was an unforced error (u) using the forehand (fh) volley (v) and the shot was played into the net (n).

Each input is divided into 6 categories:

1. Serve (1st or 2nd serve)
2. Player (1-4)
3. Main Category (Unforced error, Forced winner, Winner)
4. General Shot Side (e.g., backhand, forehand, high contact, High Defense)
5. Specific Shot Type (e.g., volley, vibora, smash)
6. Shot Direction (e.g., net, cross, parallel)

In the following table, all the possible combinations of shots and their abbreviations are given.

| Serve | Player      | Main Category          | General Shot Type | Specific Shot Type | Shot Direction   |
|-------|-------------|------------------------|-------------------|--------------------|------------------|
| e     | 1st Serve   | 1 Player 1 (Right side team 1) | u Unforced Error | fh Forehand        | v Volley         | p Parallel      |
| t     | 2nd Serve   | 2 Player 2 (Left side team 1)  | f Forced Winner* | bh Backhand        | n Normal (without the backwall) | c Cross |
|       |             | 3 Player 3 (Right Side team 2) | w Winner         |                   | g Glass (with the backwall) | n Net |
|       |             | 4 Player 4 (Left side team 2)  |                 |                   | hi High Contact  | s Smash        | l Long |
|       |             |                               |                 |                   | hd Defense of High contact | k Kick | M Middle |
|       |             |                               |                 |                   |                  | b Bandeja      | k Dunk |
|       |             |                               |                 |                   | v Vibora         | d Dropshot     |
|       |             |                               |                 |                   | j Bajada         | g Lob (globo)  |
|       |             |                               |                 |                   |                  | f Fence        |

The first 3 categories are general categories and are universal for each input, for categories 4 and 5 there are specific pairings that are used (shown in colour). For example, the input “hdv” (“hd” – Cat4 and “v” – Cat5) would be a High Defense of a Vibora whereas the input “fhv” would be a forehand volley, the “v” is contextual and depends on the previous input.

For any input to be valid and accepted by PyPadel it must contain one code (abbreviation) of each of the 6 categories. If not, it will display an error message.

*Forced winners – The following is an example of an input for a forced winner – “e1ffhvm3bhg”. There are 3 additional categories added to the input. For forced winners, we take 2 shots into account – the first is the shot that forced the error out of the opponents (“e1ffhvm” – player 1 played a forehand volley to the middle) and the second is the shot played by the opponents that was missed (“3bhg” – player 3 missed a backhand played after the glass).

## Contributing

Contributions to PyPadel are welcome! Whether it's bug reports, feature requests, or code contributions, feel free to open an issue or submit a pull request.

## License

PyPadel is open-source software licensed under the Apache 2.0 license.
