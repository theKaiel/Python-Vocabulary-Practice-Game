# Vocabulary Practicing Game
A simple game to practice vocabulary words by selecting the correct meaning of the given word.

- Python GUI

  - module: *tkinter*
  - main objects used: *Frame*, *Button*, *ScrolledText* etc.

- Interaction Flows

  - Record vocabulary and its part of speech, meaning, and weight in CSV files(.csv) under the "vocab" directory
    - weight = 0: randomly choosed
    - weight = 1: must choosed
  - Start the game
  - If there're any wrong answers, the vocabulary words will be displayed on the score page and recorded in a text file(.txt) under the "history" directory

- Reference

  - Color palette: https://www.canva.com/colors/color-palettes/rosy-dew/
  - Vocabulary: https://sites.google.com/a/ms2.cdjh.hc.edu.tw/english2012/

## Version 1.0
- Manual: User should put their vocabulary words in CSV files under directory "vocab" with 4 must-be-correctly-ordered columns, *vocab*, *type*, *meaning*, and *weight* before the game's started.

- Necessary installation
  ```
  pip install tk
  pip install pandas
  pip install numpy
  ```

- Demo video: https://youtu.be/5rxIzEcMu1M

- Some new features may be added in the future
  1. User is allowed to choose files directly before each round
  2. Another GUI for generating the CSV files
