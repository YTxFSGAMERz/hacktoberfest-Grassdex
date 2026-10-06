# Field test results

## Accuracy

- Snaps logged: 29, rated: 17, unrated: 12
- Right / close / wrong: 11 / 5 / 1
- Strict accuracy (right only): 11/17 = 65% (95% CI 41-83%)
- Lenient accuracy (right or close): 16/17 = 94% (95% CI 73-99%)
- Abstained (unknown, unsure, or confidence 10 or less): 1 of 29
- Parse failures (model output was not valid JSON): 0 of 29

## Confidence check

- Mean reported confidence when right: 96
- Mean reported confidence when close: 93
- Mean reported confidence when wrong: 95

If wrong answers carry similar confidence to right ones, say that confidence is not trustworthy.

## Latency (seconds per snap)

- Median 16.1, p90 18.4, max 36.3, min 9.7
- First snap 10.1 (cold start is likely)

## By kind

| Kind | Rated | Right | Close | Wrong | Strict accuracy |
|---|---|---|---|---|---|
| bird | 3 | 2 | 1 | 0 | 67% |
| bug | 3 | 2 | 1 | 0 | 67% |
| fungus | 2 | 1 | 1 | 0 | 50% |
| plant | 9 | 6 | 2 | 1 | 67% |

## Bingo

- Snaps checked against a square: 14
- Model said the square matched: 4
- Squares done: 3 of 9, of which overridden by the player: 2
