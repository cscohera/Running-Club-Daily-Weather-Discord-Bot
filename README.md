# Discord Bot that gives daily weather updates to determine if practice is happening or not

Made this Bot to tell UCF club runners the weather. This was done so that if I forgot to check Thorguard (the weather system used by UCF) club members would still know if practice was happening or not.



<br />
<br />

# The Bot started off very simple with me learning the basics
<br />
<br />
I wanted to get my data from UCF's weather system Thorguard as that determines if we have practice or not. After doing some research I found I need to webscape as they did not have a API for me to pull from.
<br />
<img width="596" height="159" alt="Screenshot 2025-08-14 at 4 34 18 PM" src="https://github.com/user-attachments/assets/7689c001-7b4b-4163-b88b-93da94e1c9e8" />


<br />
<br />


Once I was able to figure out what I wanted to display I started to perfect it.
<br />

<img width="472" height="214" alt="Screenshot 2025-08-14 at 4 34 45 PM" src="https://github.com/user-attachments/assets/4ac772aa-5979-4d1d-9235-a53368912820" />
<br />
<br />
This is when I ran into a larger problem when I had a few other officers test the bot. I couldn't pull information fast enough and multiple requests would mess up the formatting of the bot. Additonally, I hit a rate limit from discord which were to major things I needed to fix. 

In order to fix both of these issues I decided to start caching weather info for 30 seconds so that if someone asks for the weather it will take the first request and requests after which will be ignored inorder to not send out unneed requests. 
<br />
<br />
<img width="623" height="418" alt="Screenshot 2025-08-14 at 4 33 30 PM" src="https://github.com/user-attachments/assets/348ac6d6-02d0-4cff-9391-b82a64c15479" />
<br />
<br />
Another example of bot breaking with multiple requests:
<br />
<br />
<img width="606" height="548" alt="Screenshot 2025-08-14 at 4 36 04 PM" src="https://github.com/user-attachments/assets/8db959d0-f791-4640-8736-39b5cdf65e6f" />
<br />
<br />

Here you can see the corrected solution. This was a great solution that solved both problems and one I'm very happy with.
<br />
<br />
<img width="580" height="545" alt="Screenshot 2025-08-14 at 4 36 59 PM" src="https://github.com/user-attachments/assets/93744cf7-c9e8-4036-9d79-e5c1cee929c9" />

<br />
<br />
Final product: Bot can display weather at any time with the !weather command and I have also created a loop command that will display the weather 45 mins before practice everyday.
<br />
<br />
<img width="525" height="274" alt="Screenshot 2025-08-14 at 4 45 22 PM" src="https://github.com/user-attachments/assets/31e93e95-16cb-43fc-b5d7-d764c36ebb07" />
<br />
<br />

# This leads into WeatherBotV2 

After some feedback and my personal need to refine this project, I decided to make this bot faster, cleaner, and easier to use for users.
This led me to finding that there was in fact a api that thorguard was using I just needed to look more. 

<br />
<br />

<img width="1371" height="529" alt="Screenshot 2025-09-18 at 11 24 19 AM" src="https://github.com/user-attachments/assets/c14682b4-0623-4887-9493-c053f79667eb" />
<br />
<br />

I went on to remove webscraping and stopped using selenium. Testing api was much faster fixing delay issues. Below contains the json data I needed for this project.
<br />
<br />

<img width="1435" height="132" alt="Screenshot 2025-09-18 at 11 46 25 AM" src="https://github.com/user-attachments/assets/05140ca3-bdd5-42b0-ac6b-c24e6aabb20a" />
<br />
<br />

From here I needed to convert the json into a python dict in order to easily access each individual piece of weather information. 
<br />
<br />
<img width="1121" height="519" alt="Screenshot 2025-09-18 at 11 51 33 AM" src="https://github.com/user-attachments/assets/89ceddb3-756a-4445-9830-6c3e3e5f305a" />
<br />
<br />
Next, with this new information I began working on the /command which will be much easier for Knight Runner officers to tell runners if practice is happening. I had some issues early on converting the json but I figured out quickly it was layered into the ['23-08-30-010']. I also had to do more research into discords documentation to learn how to implement a / command and only allow it for officers so not all users could spam the command. Below you can see some of my implementation. I also added features to display the current time correctly. The big change to using a / command needed to use embeds. I also had to change both the daily weather and command function as the / command needed to be a interaction and before I was using ctx which did not work well with /commands. 
<br />
<br />
<img width="1086" height="710" alt="Screenshot 2025-09-18 at 12 25 28 PM" src="https://github.com/user-attachments/assets/3b81dfef-797a-4917-9891-a5e6a2135fd0" />
<br />
<br />
From here I worked on making the embeds look good as well as fixing some bugs with the time and api. The command works so much faster and works for any officer in any channel needed.

<img width="622" height="381" alt="Final_product" src="https://github.com/user-attachments/assets/cb386187-411c-4d80-bd2d-153b7de973aa" />

<br />
<br />
To host this bot I have digital ocean droplet that I run the python through linux screens. Posting this bot I also learned the dangers of hardcoding my bot info as I forgot to remove it and accidentlly leaked my old discord bot code. I quickly learned to changed this to be using a .env file to protect this critical information.

# Skills I learned from this

<ul>
      <li class="indiv_skills">Stronger Python Knowledge</li>
      <li class="indiv_skills">Drawbacks of Webscraping and benefits of using APIs</li>
      <li class="indiv_skills">How to convert raw json to python dict to interpret data</li>
      <li class="indiv_skills">How to use Screens,.env files, and digital ocean to host the bot securly</li>
      <li class="indiv_skills">Caching data, rate limiting, bot permissions</li>
    </ul>





