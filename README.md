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
#### Stage 1
I have obtained the data on each individual player to ever participate in a KHL match. This includes not only personal information such as age and weight but also the statistics for every season that player has played at least one match in and every match he has played in.

The season data is separated into Regular season and Playoff, since the two present a rather different style of play and not all players enjoy the opportunity of their team making it into the playoffs. Additionally, there is a third type for off-season tournaments which are not considered to be official matches and are thus absent from the player's match data.

In case the data becomes too heavy to be hosted on GitHub anymore (which the match performance dataset is getting close to), I have uploaded it to Kaggle with the following link: https://www.kaggle.com/darkhobbit/kontinental-hockey-league-khl-player-performance.

The data have also been uploaded to an AWS-hosted PostgreSQL database. Connect through projects.cztadsor7fc9.eu-central-1.rds.amazonaws.com by using "guest" as both login and password.

#### Stage 2
Most of the data was coriginally not in very suitable format to do anything with it. To begin with, I have separated the season data into career statistics and actual season statistics. After that, a number of changes were introduced to the dataset.

First of all, a lot of players were present in the match-level data but had no actual statistics and absent icetime. We are naturally not interested in such data, as those players have effectively not participated in the match. A small number of data points actually had proper statistics recorded but not the icetime, such observations were omitted as well. Two matches were completely dropped from the data: Vityaz - Avangard on January 9th 2010 and Slovan - Vityaz teams on January 11th 2019.

Next, the performance indicators are different for skaters (forwards and defencemen) and goalies (goalkeepers). Therefore, the data were separated into two dataframes for each period of interest (career/season/match). That allowed to get rid of the columns that are not relevant to a specific player and somewhat reduce the file sizes.  

Most numeric values in the raw data files were also stored as floats and some even as objects. I have changed most of the values to integers (where applicable), in big part due to the separation of skaters and goalies. 

Finally, the data in some columns of the original tables was split into multiple columns each. That includes Season (career/season/match), Teams (match) and Score (match). New columns for created in the match-level data, containing the player's team name, the name of a winning team and unique match ID. For both the icetime per game and total icetime a new column was created, stored as integer containing the icetime in seconds.

Important note: Hits, Shots blocked and Penalties against were not recorded in the KHL until season 2014/2015. I have decided to keep them as null values rather than replace with zeros, to avoid accidentally using the values in an analysis. However, that is something to be kept in mind.

The data have been uploaded to an AWS-hosted PostgreSQL database as mentioned in the previous stage.

### In work
#### Match winner predictions
I am currently playing with the idea of aggregating player dummies into a team-level data for each match. That way, we can train the model to try and predict the outcome of a match based primarily on the player roster of the two teams (and some added features such as year). Those dummies could be multiplied by the prospective player's average icetime. Such an analysis would question how much of a team's success is attributed to their roster and how much to the staff in charge of the team. In addition, using polynomial features would allow us to try and catch the synergy between players. And, of course, we could compare the levels of effect different players have on their team's success.

So far, the analysis is not showing any satisfactory accuracy. The first results of the simplest version of model were actually not that bad on paper, several slightly different versions achieving close to 60-62% accuracy with a much better performance on home wins - around 60% precision and 80% recall for an f-score of 0.68. However, the way those models were designed does not allow us to rely on the results since they only had dummies for individual players and for specific years, but not for an individual player in a specific year.

Effectively, it is a single dummy variable for a player over his whole KHL career which is obviously not the right way to go. Separating it into multiple dummy variables drastically reduces the number of observations for each one of them, reducing the model's accuracy as well. A number of approaches all give approximately the same results. I still intend to test out the idea some more using different classification models, and taking the icetime into account. However, I am now going to move the idea into a separate branch to test out when a better implementation comes to mind. 

#### Season points prediction
Another idea in the works is trying to predict a player's season performance based on his performance in the past several seasons. Specifically, the first target variable of interest is how many points a player will get over the season. To better account for the fact that not all players get the same icetime, I have tried using the measure of points per hour of icetime.

This idea has taken around a week of work and several dozen different approaches by now, with both simple and complex models often yielding similar-looking results. From the analysis it appears that predicting season performance off the past three seasons seems to be the most accurate, as it performs the best when used in a simple benchmark such as average number of points per hour over 1/2/3 seasons.

Such a benchmark, used with a 3-year period, already performs with the RMSE (root-mean-square error) of around 0.49-0.5 points per hour. The best results I have managed to get with Machine Learning so far had the RMSE of around 0.48-0.49 points per hour, only slightly better than the benchmark mentioned above. This appears to be due to inherent variation in the data that complicates the use of Machine Learning models, including a fairly small number of high-performing players that the models tend to severely underestimate.

The main factor is perhaps the inequality in the teams' strength, with some teams having consistently better results than the others in terms of the individual players' performance. The difference can reach up to 0.3 points per hour between the average players of two different teams. And while capturing such a gap is exactly the thing we are looking for, having to account for the much more frequent changes of teams in KHL compared to NHL significantly drops the number of observations. After all, we not only need dummy variables for every team but actually for every team for every of the 2/3/4 seasons (including the current one) that we are considering in our analysis.

Therefore, this analysis is going to be suspended as well until I find a better way to handle it. 

### Further plans
In the future, I am also going to attempt scraping the history of each team's matches over time the same way as was done for the players.

The KHL website might not store the necessary data in an easy-to-access form. In that case, we can take an approach of reconstructing the statistics for a match by aggregating the statistics of each individual player that took part on it.

## Materials used
All data used in this project belong to the KHL and were taken from the league's website, https://en.khl.ru/.