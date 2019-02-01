# Finding the Two Best Markets to Advertise in an E-learning Product
# In this project, we'll aim to find the two best markets to advertise our product offering courses on programming. 

# Overview of the Data
# To avoid spending money on organizing a survey, we'll first try to make use of existing data from 
# freeCodeCamp's 2017 New Coder Survey to determine whether any reliable result.
# freeCodeCamp is a free e-learning platform that offers courses on web development. 
# Their survey attracted new coders with varying interests (not only web development), ideal for the purpose of our analysis.

# Reading in the data
import pandas as pd
direct_link = 'https://raw.githubusercontent.com/freeCodeCamp/2017-new-coder-survey/master/clean-data/2017-fCC-New-Coders-Survey-Data.csv'
fcc = pd.read_csv(direct_link, low_memory = 0) # low_memory = False to silence dtypes warning

# in the raw-data folder of the repository are the initial survey questions:
# (and from there it should be easy to infer what each column describes)
#,"Are you already working as a software developer?","Is this your first software development job?","Before you got this job, how many months 
# did you spend looking for a job?","Would you prefer to...","Full-Stack Web Developer","Back-End Web Developer","  Front-End Web Developer","  
# Mobile Developer","  DevOps / SysAdmin","  Data Scientist","  Quality Assurance Engineer","  User Experience Designer","  Product Manager",
# "Game Developer","Information Security","Data Engineer",Other,"When do you plan to start applying for developer jobs?","About how much money 
# do you expect to earn per year at your first developer job (in US Dollars)?","Would you prefer to work...","Are you willing to relocate for a 
# job?",freeCodeCamp,EdX,Coursera,"Khan Academy","Pluralsight / Code School",Codecademy,Udacity,Udemy,"Code Wars","The Odin Project",Treehouse, 
# Lynda.com,"Stack Overflow",W3Schools,Skillcrush,HackerRank,"Mozilla Developer Network (MDN)",Egghead.io,"CSS Tricks",Other,"freeCodeCamp study 
# groups",hackathons,conferences,workshops,"Startup Weekend",NodeSchool,"Women Who Code","Girl Develop It","Meetup.com events",RailsBridge,"Game Jam",
# "Rails Girls","Django Girls","weekend bootcamps",Other,"Code Newbie","The Changelog","Software Engineering Daily","JavaScript Jabber","Ruby Rogues",
# "Shop Talk Show","Developer Tea","Programming Throwdown",".NET Rocks","Talk Python To Me","JavaScript Air","The Web Ahead","CodePen Radio","Giant 
# Robots Smashing into Other Giant Robots","Software Engineering Radio",Other,"MIT Open Courseware","The New Boston",freeCodeCamp,Computerphile,DevTips,
# "Engineered Truth",LearnCode.Academy,CodeCourse,LevelUpTuts,funfunfunction,"Coding Tutorials 360","Coding Train (Coding Rainbow)","Derek Banas", 
# Simplilearn,"Mozilla Hacks","Google Developers",Other,"About how many hours do you spend learning each week?","About how many months have you been 
# programming for?","Have you attended a full-time coding bootcamp?","Which one?","Have you finished yet?","Did you take out a loan to pay for the 
# bootcamp?","Based on your experience, would you recommend this bootcamp to your friends?","Aside from university tuition, about how much money 
# have you spent on learning to code so far (in US dollars)?","Start Date (UTC)","Submit Date (UTC)","Network ID"

# Exploration of the data
print(fcc.shape)
pd.options.display.max_columns = 150  
fcc.head()

# Checking for Sample Representativity
# we want to answer questions about a population of new coders that are interested in the subjects we teach. 
# We'd like to know:
# -Where are these new coders located.
# -What locations have the greatest densities of new coders.
# -How much money they're willing to spend on learning.

# 1.Clarify whether the data set has the right categories of people for our purpose. 
# 2.The JobRoleInterest column describes for every participant the role(s) they'd be interested in working in. 
# 3.If a participant is interested in working in a certain domain, it means that 
# they're also interested in learning about that domain. So let's take a look at the frequency distribution 
# table of this column and determine whether the data we have is relevant.

# Frequency distribution table for 'JobRoleInterest'
fcc['JobRoleInterest'].value_counts(normalize = True) * 100

# A bit of a review...

# Many are interested in web development (full-stack web development, front-end web development and back-end web development).
# A few people are interested in mobile development.
# A few people are interested in domains other than web and mobile development.
# It's also interesting to note that many respondents are interested in more than one subject. It'd be 
# useful to get a better picture of how many people are interested in a single subject and how many have 
# mixed interests. We will:

# Split each string in the 'JobRoleInterest' column to find the number of options for each participant.
interests_no_nulls = fcc['JobRoleInterest'].dropna() #drop the null values because we can't split Nan values
splitted_interests = interests_no_nulls.str.split(',') 

# Frequency table for the variable describing the number of options
n_of_options = splitted_interests.apply(lambda x: len(x)) # x is a list of job options
n_of_options.value_counts(normalize = True).sort_index() * 100

# 31.7% of the participants have a clear idea about what programming niche they'd like to work in, 
# while the vast majority of students have mixed interests. But given that we offer courses on various 
# subjects, the fact that new coders have mixed interest would be good for the company.

# Frequency table choosing between web vs mobile
web_or_mobile = interests_no_nulls.str.contains(
    'Web Developer|Mobile Developer') # returns an array of booleans
freq_table = web_or_mobile.value_counts(normalize = True) * 100
print(freq_table)

# Graph for the frequency table above
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

freq_table.plot.bar()
plt.title('Most Participants are Interested in \nWeb or Mobile Development',
          y = 1.08) # y pads the title upward
plt.ylabel('Percentage', fontsize = 12)
plt.xticks([0,1],['Web or mobile\ndevelopment', 'Other subject'],
           rotation = 0) # the initial xtick labels were True and False
plt.ylim([0,100])
plt.show()

# 86 % of people are interested in either web or mobile development, giving strong reason to consider this sample representative for our population of interest
# as we seek to sell this type of product. 

#  We are looking to discover the following:
# 1. the best markets to invest money in for advertising our courses
# 2. locations these future engineers are seeking these opportunities in learning
# 3. also the locations with the greatest number of current practictioners of the trade
# 4. the amount new students are willing to spend to learn

# Here we seek the best countries as our locations of interest

# Isolate those who answered what role they'd be interested in
fcc_good = fcc[fcc['JobRoleInterest'].notnull()].copy()

# Frequency tables with absolute and relative frequencies 
# CountryLive is where we find the locale of surveyed persons country
absolute_frequencies = fcc_good['CountryLive'].value_counts()
relative_frequencies = fcc_good['CountryLive'].value_counts(normalize = True) * 100

# Reframe to be more readable
pd.DataFrame(data = {'Absolute frequency': absolute_frequencies, 
                     'Percentage': relative_frequencies}
            )

# 45.7% of our potential customers are in the US, and so this is the market to reach first. India is second at 7.7%, 
# the United Kingdom at 4.6% and Canada's 3.8%.

# Then determining how much each student is willing to pay to learn:
# MoneyForLearning - the amount of dollars spent by surveyed persons already 
# Note: the initial projected company product price is $59 USD a month

# Divide the MoneyForLearning column by the MonthsProgramming column; Some students answered they've been learning 
# to code for 0 months so to avoid dividing by 0, 0 is replaced with 1 in the MonthsProgramming column.

fcc_good['MonthsProgramming'].replace(0,1, inplace = True)

# New column to account for spending for each student each month
fcc_good['money_per_month'] = fcc_good['MoneyForLearning'] / fcc_good['MonthsProgramming']
fcc_good['money_per_month'].isnull().sum()
fcc_good = fcc_good[fcc_good['money_per_month'].notnull()] #keeping rows w/o null values
fcc_good = fcc_good[fcc_good['CountryLive'].notnull()] #same as above applied to CountryLive
fcc_good['CountryLive'].value_counts().head()  #check for available data
countries_mean = fcc_good.groupby('CountryLive').mean() #average spent per month corresponding to country of origin
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]                   #sort by country

only_4 = fcc_good[fcc_good['CountryLive'].str.contains(       ## box plots of the distribution of the money_per_month variable for each country
    'United States of America|India|United Kingdom|Canada')]
import seaborn as sns
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada'])
plt.show()

fcc_good = fcc_good[fcc_good['money_per_month'] < 20000]  # Isolate only those participants who spend less than 20000 per month
countries_mean = fcc_good.groupby('CountryLive').mean()   # Recompute mean sum of money spent by students each month
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]

only_4 = fcc_good[fcc_good['CountryLive'].str.contains(
    'United States of America|India|United Kingdom|Canada')]

sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada'])
plt.show()

india_outliers = only_4[                    # Inspecting extreme outliers for India as they spend hefty $2500+
    (only_4['CountryLive'] == 'India') & 
    (only_4['money_per_month'] >= 2500)]
india_outliers       # they may have included university tuition in their response -> unnecessary for our project purposes

only_4 = only_4.drop(india_outliers.index) # remove the outliers for India using the row labels

us_outliers = only_4[                                       # Examine the extreme outliers for the US values over $6000 per month
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000)]

us_outliers

# There were 11 extreme outliers in the US case. Large sums spent by 6 of which are confirmed to be due to bootcamps. 
# The remaining 5 are inconclusive as to the origin of their spending to learn as they do not further contribute to 
# providing a good average of what students, on average, spend a month on software development learning courses.

# Another point of interest is 8 recipients of the survey coding for three months or less. The likelihood of this excess spending is 
# due to signing up for an ongoing bootcamp program. This information is again unnecessary for our purposes. 

# Removing respondents who didn't attendent a bootcamp
no_bootcamp = only_4[
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000) &
    (only_4['AttendedBootcamp'] == 0)
]

only_4 = only_4.drop(no_bootcamp.index)

# Removing respondents programming for less than 3 months
less_than_3_months = only_4[
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000) &
    (only_4['MonthsProgramming'] <= 3)
]

only_4 = only_4.drop(less_than_3_months.index)

# Examine the extreme outliers for Canada
canada_outliers = only_4[
    (only_4['CountryLive'] == 'Canada') & 
    (only_4['money_per_month'] > 4500)]

canada_outliers

only_4 = only_4.drop(canada_outliers.index) # Encountered same issues as with US so remove the extreme outliers for Canada

only_4.groupby('CountryLive').mean()['money_per_month'] # Recompute mean

sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
          fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) 
plt.show() # Visualize final distributions 

# Conclusion

# The main country to advertise in is the US. 
# The majority of student developers seek education here and are willing to pay, on average, each month $143 
# -- much more than our product demands --making it a win-win deal. 
# 
# The e-product intended for market would go for $59 per month, and so Canada also is a strong contender to reach 
# as prospective students are willing to pay roughly $93 per month. 
# In India it's $66 and in the United Kingdom it's $45.

# The data therefore concludes not to advertise in the UK. In India, it appears a fair shot as $59 is a middle of the 
# road average spending sum of $66 each month. 
only_4['CountryLive'].value_counts(normalize = True) * 100 # Frequency table for CountryLive 

# There is a good chance India is a better choice due its large number of potential customers (7.7%) compared to those we found 
# earlier for Canada (3.8%).

# Resulting Options:
# (1) Advertise in the US, India, and Canada splitting the advertisement budget in various capacities
# (2) Advertise only in the US and India, or the US and Canada unequally
# (3) Advertise only in the US.

# The analysis is best further utilized by the marketing team whose skillset would be utilized  in administering surveys to decide
# which option provides the best opportunity for the outreach. 
