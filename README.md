# Most Improved Player (MIP) Award Prediction Project

This project aimed to predict the winner of the NBA’s **Most Improved Player (MIP)** award using machine learning models and statistical analysis. While some predictions were successful, the overall challenge of accurately predicting the MIP winner across multiple seasons proved more complex than initially expected.

## Challenges Encountered

### Correlation Between Features and MIP Share
The primary challenge was finding strong correlations between the feature variables (e.g., player and team statistics) and the MIP share. Unlike other awards, the MIP selection process appears more subjective and context-driven, making it harder for models to generalize across different years.

### Ambiguity in Award Criteria
The MIP award is defined as honoring an "up-and-coming player who has made a dramatic improvement from the previous season or seasons." This creates ambiguity in how voters interpret "improvement" and how much weight they place on a player's **entire career** versus their **most recent season**. Both need to be considered in the model, which complicates the feature selection and prediction process.

#### Examples:
- **Channing Frye (2009-10):** Despite improving his averages, his prior strong rookie season may have diminished his MIP candidacy.
- **Coby White (2023-24):** Finished second in MIP despite a stronger season in 2020-21, indicating how inconsistent past performance can affect the voting outcome.

### Open Interpretation of "Dramatic Improvement"
What constitutes "dramatic improvement" can vary. Typically, it relates to a player’s points per game (PPG) increase, but exceptions exist:
- **Dorell Wright (2010-11):** Finished 3rd in MIP voting despite a significant increase in PPG and a better team performance.
- **Kevin Love (2010-11):** Won the award with a smaller PPG increase but a standout rebounding performance, even though his team had the worst record in the league.

### Team Performance Influence
Another layer of complexity is the weight voters place on **team success**. Some years, team performance is crucial, while in others, it appears irrelevant:
- **Kevin Love (2010-11):** Won despite the Timberwolves' poor record (17-65).
- **Giannis Antetokounmpo (2016-17):** Won over Nikola Jokic, likely due to the Bucks making the playoffs, while Denver missed them, despite Jokic having better individual improvements.

## Conclusion

Predicting the MIP award is significantly harder than predicting other awards, such as **MVP**. While MVP decisions can typically be made based on team and individual performance from a single season, MIP winners may be influenced by a combination of performance across multiple seasons. This variability makes it tough to create a consistent model for the MIP winner over many years.

### Future Directions
- **Exploration of Voter Patterns:** Analyze voting trends to better understand how voters weigh career performance versus recent seasons.
- **Feature Engineering:** Improve feature selection by focusing on players' full career arcs, team dynamics, and narrative-driven factors.

## Inspiration
- This project was inspired by an NBA MVP prediction model initially developed by Gabriel Pastorello here: https://towardsdatascience.com/predicting-the-nba-mvp-with-machine-learning-c3e5b755f42e. His work on using machine learning to predict NBA MVP winners was pivotal in shaping the approach and methodology used in this NBA MIP model.

---

This project provided valuable insights into the complexities of predicting subjective awards and highlighted areas for future improvement in both modeling and understanding of the award process.