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
  - Vocabulary: http://download.bestdaylong.com/f675.htm

## Version 1.*
- Manual: User should put their vocabulary words in CSV files under directory "vocab" with 4 must-be-correctly-ordered columns, *vocab*, *type*, *meaning*, and *weight* before the game's started.

- Extracting rate: 0.5
- Number of choices: 5

- Necessary installation
  ```
  pip install tk
  pip install pandas
  pip install numpy
  ```

- Demo video: https://youtu.be/5rxIzEcMu1M

- Some new features may be added in the future version
  1. <font color=#555555>User is allowed to choose files directly before each round</font> Done in Version 1.2.
  2. Another GUI for generating the CSV files

### Version 1.1
- update: vocabulary words and meanings in all languages are supported.
### Version 1.2
- update: users ought to choose files each round before the game's started.

