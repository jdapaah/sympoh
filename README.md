# Repository of Code for Managing Sympoh Breaking Crew

This repository contains code used to better manage Sympoh Breaking Crew. It seeks to accomplish tasks such as tracking sess, optimizing casting and rehearsal schedules, and the like.

## Commands
### PlaceK `k`
Place everyone in solely their kth choice piece.
Show casting, evaluate happiness metric
### View `member`
* Member (name | id):
    * ID (3Alpha)
    <!-- * Name -->
    * Happiness Metric
    * Number of pieces
    * Prefered number of pieces
    * Current Pieces
    * Prefered Pieces
### View `cast`
* piece (id):
    * ID(2Num)
    * List of Members
    * Size of Cast
    * Prefered size of cast

### Add `member` `cast`
Add `member` to `cast`
Checks: `member` already in `cast`
### Remove `member` `cast`
Add `member` to `cast`
Checks: `member` not in `cast`
