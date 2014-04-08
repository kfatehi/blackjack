## hardcoded values

* they make it hard to follow the code.
e.g. blackjack.py line 137 it is unclear what the significance of 14 is.

* it doesn't cost anything to name these values at least to improve readability.
e.g. line 116 you shuffle at 35 percent. we can improve readability and configurability
by putting harded values into a dictionary/hash structure:

```python
  config = {
    capacityForShuffle: 0.35,
    deckCards: {
      A:14
    }
  }
```

with this, you can just reference off your config which makes things readable and maintainable.

## testing

I noticed this:

```python
c = self.game_deck.drawCard()
self.player_hand.addCardToHand(c)
self.player_hand.addCardToHand(c)
```

that's a stone's throw away from being the start of a test harness.
a specification, spec, or test, will test the behavior of, say, the player_hand or the game_deck,
this begins with instantiating it, and setting up some state, like you have, and then asserting that
some value is some expected value.

## consistency

line 187 you go 'print' on a line by itself but then on line 195 you print a string and then + '\n' -- it's generally better to stay consistent. personally i think the print on a line by itself looks better, but some would say that's a performance hit, but im not gonna go write a benchmark to find out of adding a character to the string or making another call to print is more optimal... 


## other than that

looks really good. judging by your ability to use github and your working knowledge of python (e.g. newbies dont know how to setup a loop with a runflag like you do in line 353-364. and maybe less know about 369-371)

The only things that are missing here that i would want to see from someone trying to qualify the diversity of their software developer skills to me would be:
 * using networking
 * a better UI
 * tests or better yet, evidence that the thing was built in a test-driven manner

the last one is the only one that is truly important, but it's suprising how few people share this core value, and out of those, how few that really practice it (i too am guilty... when i dont testdrive, i spend 20 minutes producing code that's 1 theoretical unit of quality. when i test drive i spend 40 minutes and produce 4 theoritical units of quality)
