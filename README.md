# MAIC2020-Yote
Third edition of the Mify Artificial Intelligence Contest #MIFY #AAAIBenin



## The Game

The game chosen for this edition is Yote. It is played by 2 players on a board generally either 6 squares out of 5 or 5
squares out of 5. Each player has 12 pieces of different colours. The aim of the game is to capture all the opponent 
pieces. More information on the competition and the rules of the game is available [here](https://maic.mify-ai.com/maic2019).

## Setup

The game was implemented in **Python** and works with versions greater than or equal to **3.6+**.

### Get Python and dependencies


You can download the **3.8** version of Python [here](https://www.python.org/downloads/).
(Don't forget to add python to the path if you are on Windows)

Next, install the dependencies for the game. For that just run the following command (Note that you may replace *pip* by *pip3* if you have different versions of python).


```bash
pip install -r requirements.txt
```

### Run the code

Firstly, just clone this repository or download the zip to get everything you need to work and just run by following the instructions.


**Usage:**

      python main.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5


      -ai0 
          path to the ai that will play as player 0
      -ai1 
           path to the ai that will play as player 1
      -s 
           time(in second) to show the board(or a move)
      -t
           total number of seconds credited to each agent


**Example:**

        git clone https://github.com/Machine-Intelligence-For-You/MAIC2019.git
        cd MAIC2019/
        python main.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5



### Allowed time for each AI
The t option allows you to specify the overall time allowed for all of you AI moves. After this time is exhausted all the next moves for the AI is done by a random agent.
Now to run it you will have to use another file which is **main.py** with the same settings.

**Example:**

         python main.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5 -t 120
