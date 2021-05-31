# KHL Data Analysis
## Overview
Sports analytics is an actively growing field. Being a hockey fan myself, I am curious to see whether I manage to extract any interesting insights from the data for the KHL (Kontinental Hockey League).

The teams in KHL are much less comparable with each other than in NHL, with many teams being severely under the salary cap. In fact, for several KHL teams their budgets are less than half of the salary cap. Naturally, this creates a discrepancy in the teams' performance that affects how well the players perform on the ice.

Is a player's statistic for a season good because of his skills and talent, or because he played games in a wealthy team with many talented players? How could we adjusted the season statistics to account for it? That question is at the core of this project with an ultimate goal of dissecting the role of a team in the individual players' achievements.

In addition, contracts in KHL tend to be relatively short-term for both the players and the staff. As such, they have less time to gain experience of playing together and might depend even more on how well the coaches can adapt to the constantly changing teams. Analysing the roles of coaches in their team's season performance is one of the other goals of this project.

## Player-level analysis
There are many different things you can ask the data about here.

How indicative is the player's performance in past seasons of his potential in the next one? How many seasons should we take into consideration? How much changing a team affects the performance? Those questions, and many more, are going to be raised in this project.

It is also possible to deeper look at specific players' performance metrics. Having a match-level data would give us enough data points to plot them over time and analyse the trends in an easier way. Perhaps a player is a very unstable one, prone to having periods of either outstanding performance or a terrible one.

## Team-level analysis
Here, my aim is to gather more data to include both the coaches and the individual players into the models that predict the outcome of a match. The main interest in such analysis is potentially being able to tell how well a team is performing compared to what their roster would suggest.

On a very different yet important note, there already exists a system for evaluating the possible  outcomes of the match. It is called betting. The betting odds represent the probabilities of such events happening, so it would be very interesting to later compare our analysis against it.

One way it could be compared is by using the created model before a new match to predict the outcome. Luckily for us, the KHL teams announce their roster some time before the match. Would our predictions be more accurate than the betting odds over a season? Who knows.

## Project life cycle
### Completed
I have obtained the data on each individual player to ever participate in a KHL match. This includes not only personal information such as age and weight but also the statistics for every season he has played at least one match in and every match that player has played in.

The season data is separated into Regular season and Playoff, since the two present a rather different style of play and not all players enjoy the opportunity of their team making it into the playoffs. Additionally, there is a third type for off-season tournaments which are not considered to be official matches and are thus absent from the player's match data.

In case the data becomes too heavy to be hosted on GitHub anymore (which the match performance dataset is getting close to), I have uploaded it to Kaggle with the following link: https://www.kaggle.com/darkhobbit/ice-hockey-khl-player-data.

### In work

### Further plans
I am no longer going to use the dataset of the game outcomes from Kaggle. Both updating it and integrating it with my player-level data could create too many problems to be a viable strategy. Instead, I am going to attempt scraping the history of each team's matches over time the same way as was done for the players.

The KHL website might not store the necessary data in an easy-to-access form. In that case, we can take an approach of reconstructing the statistics for a match by aggregating the statistics of each individual player that took part on it.

We also need to process the gathered data and prepare it for further analysis. This is particularly important for any Machine Learning models I might attempt to train on this dataset.

## Materials used
All data used in this project are courtesy of KHL and their website, https://en.khl.ru/.