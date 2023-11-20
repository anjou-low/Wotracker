## About Wotracker
Wotracker is a minimalist web app I built to track my personal workouts as an alternative to Notes which was becoming quite hard to navigate. It was also a good excuse to learn more about web development.

![Homepage](/screenshots/home.png)

### Built with
The client is built with Vue.js and the backend is a Python REST API made with FastAPI and SQLAlchemy consuming a PostgreSQL database.

### Features
#### User 
* Account creation without validation.
* Authentication using Json Web Tokens.
#### Tracking
The adopts the following hierarchical structure for storing data
* A `Workout` is composed of a _Name_, a _Date_ and a list of `Exercise`s.
* An `Exercise` is composed of a _Name_ and a list of `Set`s.
* A `Set` is composed of a _Weight_ and _Repetition_  count (the number of repetitions).

Creating a `Workout` is done by clicking the associated button after which you can edit its name by simply clicking on the text, entering the desired name and pressing _Return_.

To navigate to a specific `Workout`, simply press it on the listing, this will lead you to a listing of the `Exercise`s of the selected `Workout`. This page behaves the same way as the _Home_ page, you can add new `Exercise`s to the selected `Workout`, edit their _Name_ and navigate to their list of `Set`s.

If you want to create a new `Workout` with a structure similar to that of an already existing `Workout`, click on the three dots associated with it and click _Copy as blueprint_. This will duplicate all the data of the original `Workout` and create a reference to it ; this way, when modifying the _Weight_ or _Repetition_ field of a particular set in the copied `Workout` you will be shown your progress.

![Example exercise progress](/screenshots/exercise_diff.png)