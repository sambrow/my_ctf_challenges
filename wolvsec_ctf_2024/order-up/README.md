# Title: Order Up 1-5
## Difficulty: Medium
## Internal Notes: 
Source will NOT be provided for these challenges.

This is designed to be hosted in a "each team gets a private instance" manner.

See the CTFd folder in this repo for details on how this challenge will be spun up per team.

In CTFd, this will use the "private_challenges" custom challenge type so that it can be
spun up per team.

# Title: Order Up 1

# Description
I hope my under construction web site is secure.

Solving this will unlock a series of related challenges that ALL use the same challenge instance.

Source is not provided on purpose.

To find the first flag, find a way to view the text of the SQL query.
If you find some other flag, it will be related to one of the others in this series.

Note: Automated tools like sqlmap and dirbuster are not allowed (and will not be helpful anyway).


# Title: Order Up 2

Unlocked by solving Order Up 1

# Description

The next flag is hiding in another table.  Can you find it?


# Title: Order Up 3

Unlocked by solving Order Up 1

# Description

There is a DB user named 'flag'. To find the next flag, figure out the password for
this DB user.

The flag will be: wctf{<db-password-of-flag-user>}

Note: The password can be found in the rock you word list.


# Title: Order Up 4

Unlocked by solving Order Up 1

# Description

The next flag is inside a disk file whose name is like /flag*.txt


# Title: Order Up 5

Unlocked by solving Order Up 1

# Description

BE AWARE!!! We don't know if this is solvable.  Spend time on this at your own risk.

The last flag is inside a disk fie whose name is like /root_flag*.txt

This file can only be read by the linux root user.

However, the following has been run using root on the DB container:

```
RUN chmod u+s /bin/cat
```

So... if you can achieve Remote Code Execution, then you can use `cat` to read the contents of this disk file.


## Author
SamXML

