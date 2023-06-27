* `min-width` doesn't have a defined effect on table cells, however, you can apply its effect if you implemented a `div` inside of the cell. This will make the cell adapt on the properties of the `div`.

* 4 days into the project, and realized that I'm building a mini version of Django, just made it more flexible in terms of its structure and the admin panel configuration, at the cost of more coding.
  Though, It's kind of interesting how these blocks come together to establish a better developer experience.

* Every model you create in an ORM should have a `__table__` method. from it you can access the column names via `.columns.keys()`. This is useful instead of a noob brute force approach of getting the first record and scrap out the column names.
  
  PS. The approach will return the keys in the order which was written in the `models.py`, so you either arrange them in the `models.py`, or use a similar Django approach (implemented this one) of registering which fields you want to show via a list.

* Relative imports are one of the worst techniques to rely on when importing local files. Just run the `start_script` from the parent directory of the project and import using `project_foldername.module`.

* An ouch moment, Flask doesn't have Middleware support out-of-the-box so I had to improvise a bit. Check `auth/auth.py` -> function at #26.

* Jinja2 has access to a Flask config object that contains further functionalities of apps initialized in it.

* Reference to JSON querying in [SQLite3](https://www.sqlite.org/json1.html#jeach).

* When adding event listeners to elements in loops, don't use any defined variables used in the loop as the JS interpreter will run them depending on the last value it reaches in the last iteration.

* Flask `send_file()` method automatically defines the file size headers, and can be used for resume-able downloads.

* Learned a lot about how servers receive requests through streaming before processing. Temp directories have a lot of benefits when it comes to storing data coming from networks. I'm sure going to write a blog on that.  