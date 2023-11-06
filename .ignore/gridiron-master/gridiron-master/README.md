![Logo](gridiron.png)

Gridiron is a simple quiz platform for testing out out & training your NFL knowledge! This tool primarily leverages:

* [Flask](https://flask.palletsprojects.com/en/2.1.x/) (—for serving the single page & hosting the back-end API—) and
* [SportRadar](https://sportradar.com/) (—using their API to retrieve all sorts of league-wide details.)

[Try it out here!](http://gridiron.raftacon.io)

By default, five different question types are supported & randomly generated with each call to the `generateQuestion` endpoint:

* `"What conference are the {team} in?"`
* `"What division are the {team} in?"`
* `"What team does {player} belong to?"`
* `"Which team is in the {division}?"`
* `"Which of the following is a {position}?"`

Once an answer is selected, the question options are passed back to the `validateAnswer` endpoint & then completed on the client-side compared against the option the user selected.

## Requirements

* Python 3.10 is required since `typing` definitions using custom classes (—possibly with lists?—) is not supported in <= 3.9.
* [Registration of a trial SportRadar account](https://developer.sportradar.com/docs/read/Home) to have an API key to use.

## Usage

Install pre-requisites using pip, then just run the Flask app & navigate to `localhost:5000`:

```bash
pip install -r requirements.txt
python app.py
```

If trying to serve this in a public-facing context, a quick (but not robust) solution:

* Install `waitress` via `pip`.
* Import `serve` from `waitress` in the `app.py` file.
* Replace the Flask-based `app.run` with the Waitress' `serve` equivalent.

```python
from waitress import serve

...

# app.run(debug=True)
serve(app, host='0.0.0.0', port=80)
```

[See this useful article](https://levelup.gitconnected.com/how-to-deploy-a-flask-application-on-amazon-ec2-38837df3fa52) for more details regarding hosting Gridiron on your own.

Although `waitress` does not currently [feature TLS support](https://github.com/Pylons/waitress/blob/36240c88b1c292d293de25fecaae1f1d0ad9cc22/docs/reverse-proxy.rst), you can still [set up a reverse proxy](https://dev.to/thetrebelcc/how-to-run-a-flask-app-over-https-using-waitress-and-nginx-2020-235c) through `nginx` to finish implementing SSL.

Also, some additional details to keep in mind if hosting externally:

* Make sure to update the URLs referenced in the configuration at the top of the `gridiron.js` file from `localhost` to the public-facing URL for CORS to continue working properly.
* To prevent abuse, `refresh_cache` can only be triggered locally for force-refreshing the league data (—due to the `@local_only` tagging.)

For example:

```bash
curl http://localhost:5000/api/v1/refresh_cache
```

## Extending Questions

Additional question templates can be added, too!

1. Add the new question template underneath the `Question templating` section of `config.py`.
2. Add a new `Enum` under the `QuestionType` class of `questions.py`.
3. Since new question behavior is automatically compiled when the server starts based on the `@question` tags, simply add a new question definition in `questions.py` with the `@question` tag.
4. Append a new `elif` in `validate_data_by_type` for the answer validation handling in `frontend_services.py`.
5. In `static/js/gridiron.js`, add the corresponding behavior for passing data between the `generateQuestion` & `validateAnswer` functions.

## TODO

* Create a supplementary script for easier deployment updates in the future.
