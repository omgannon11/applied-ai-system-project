# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**
When I first started playing the game everything seems normal, but when I hit enter to enter my guess it didnt work and I had to click the Submit Guess button to submit my guess. In that first game I went through it and when I was done it said the number was -35, when it said to guess a number between 1-100. When I tried to start a new game it also was not working. I had to reload the page to start a new game. In that new game I was guessing negative numbers lower than the actually number and it said Go LOWER everytime.
Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 48           To low                 to low           to low
| 30           to high              to low             to low
| 4            to low                to low            to low

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I used Claude code to implement all the bug fixes and everything involving the code. I used chatgpt to better explain the instructions of the assignment and how to do everything. A suggestion that was correct was that the bugs I found initally where real and the AI found ways to fix them. Something that was misleading was the first tests because it did not complete every test.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
I had the cladue code chat I was in run the tests until it said that all of the tests passed. It took two times for all of the tests in created to pass
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
A rerun is the app restarting everytime the user interacts with something. A session state is how Streamlit remembers information between reruns
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I would continue to ask the AI the sort of questions and things that I tell it. It worked well for me in this so it should keep being good. I would ask a little more questions on what it is actallu doing rather than me just telling it to fix things and not explain very deeply