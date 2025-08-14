# Discord Bot that gives daily weather updates to determine if practice is happening or not

Made this Bot to tell UCF club runners the weather. This was done so that if I forgot to check Thorguard (the weather system used by UCF) club members would still know if practice was happening or not.






# The Bot started off very simple with me learning the basics

I wanted to get my data from UCF's weather system Thorguard as that determines if we have practice or not. After doing some research I found I need to webscape as they did not have a API for me to pull from.
<img width="596" height="159" alt="Screenshot 2025-08-14 at 4 34 18 PM" src="https://github.com/user-attachments/assets/7689c001-7b4b-4163-b88b-93da94e1c9e8" />





Once I was able to figure out what I wanted to display I started to perfect it.
<img width="472" height="214" alt="Screenshot 2025-08-14 at 4 34 45 PM" src="https://github.com/user-attachments/assets/4ac772aa-5979-4d1d-9235-a53368912820" />


This is when I ran into a larger problem when I had a few other officers test the bot. I couldn't pull information fast enough and multiple requests would mess up the formatting of the bot. Additonally, I hit a rate limit from discord which were to major things I needed to fix. 

In order to fix both of these issues I decided to start caching weather info for 30 seconds so that if someone asks for the weather it will take the first request and requests after which will be ignored inorder to not send out unneed requests. 
<img width="623" height="418" alt="Screenshot 2025-08-14 at 4 33 30 PM" src="https://github.com/user-attachments/assets/348ac6d6-02d0-4cff-9391-b82a64c15479" />

Example of bot breaking with multiple requests. 
<img width="606" height="548" alt="Screenshot 2025-08-14 at 4 36 04 PM" src="https://github.com/user-attachments/assets/8db959d0-f791-4640-8736-39b5cdf65e6f" />

Here you can see the corrected solution. This was a great solution that solved both problems and one I'm very happy with.
<img width="580" height="545" alt="Screenshot 2025-08-14 at 4 36 59 PM" src="https://github.com/user-attachments/assets/93744cf7-c9e8-4036-9d79-e5c1cee929c9" />


Final product: Bot can display weather at any time with the !weather command and I have also created a loop command that will display the weather 45 mins before practice everyday.
<img width="525" height="274" alt="Screenshot 2025-08-14 at 4 45 22 PM" src="https://github.com/user-attachments/assets/31e93e95-16cb-43fc-b5d7-d764c36ebb07" />
