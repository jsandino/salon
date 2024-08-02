# Hair Salon Coding Challenge

## Problem Specification

### Goal
To simulate a hair salon. 

### Rules

- The hair salon is open for 8 hours, from 9am to 5pm. 
- The program shouldn't take that long to run, so it needs to somehow simulate real time.
- When the salon opens, there are 4 hair stylists who start their shift: Anne, Ben, Carol, and Derek.
- Customers arrive evry 7 minutes and are named successively starting at Customer-1. 
- When a customer enters, if a stylist is available, they immediately start cutting the customer’s hair. Otherwise, the client waits for a stylist. 
- A stylist can only cut one person’s hair at a time, and takes 30 minutes to do so.
- After a stylist is done with a customer, the customer leaves satisfied. 
- Stylists can go home after 5pm. They end their shift as soon as they can, unless they are busy with a client. In that case, they wait until they finish with that client, and then end their shift. 
- When all the stylists and customers have gone home, the salon closes. If there are any customers left waiting for a stylist, they are kicked out, and leave furious.

### Input/Output
Your program should print events in chronological: [Time] is salon-time in the format HH:MM, not real time.

#### Sample output:

```
09:00 Hair salon opened
09:07 Customer-1 entered
09:07 Anne started cutting Customer-1’s hair
09:14 Customer-2 entered
...
09:37 Anne ended cutting Customer-1’s hair
09:37 Customer-1 left satisfied
...
```
## Usage

```
make run
```

