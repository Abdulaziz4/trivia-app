# Trivia API

This is a super fun game where you can play with your friends the trivia quiz and test your knowlege in many fields and categories such as Science, Art, History and a lot more 🤩.

In this game you can:

- Display questions - both all questions and by category. Questions will show the question, category and difficulty rating by default and can show/hide the answer.
- Delete questions.
- Add questions.
- Search for questions based on a text query string.
- Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Installing Dependencies

Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

    npm install

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

    pip install -r requirements.txt

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000/) to view it in the browser. The page will reload if you make edits.

    npm start

## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET /categories

- General:
  - Returns a list of all categories
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    "categories": [
        {
            "1": "Science"
        },
        {
            "2": "Art"
        },
        {
            "3": "Geography"
        },
        {
            "4": "History"
        },
        {
            "5": "Entertainment"
        },
        {
            "6": "Sports"
        }
    ]
}
```

#### GET /questions

- General:
  - Returns a list of questions objects, current category, list of all categories, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```
{
"categories": [
		{
			"1": "Science"
		},
		{
			"2": "Art"
		},
		{
			"3": "Geography"
		},
	],
	"currentCategory": "",
	"questions": [
	{
		"answer": "Agra",
		"category": 3,
		"difficulty": 2,
		"id": 15,
		"question": "The Taj Mahal is located in which Indian city?"
	},
	{
	"answer": "Escher",
	"category": 2,
	"difficulty": 1,
	"id": 16,
	"question": "Which Dutch graphic artist–initials M C was a creator 			  of optical illusions?"
	},
],
"totalQuestions": 18
}
```

#### DELETE /questions/id

- General:
  - Deletes a question by id using url parameters.
- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

  ```
   {
   "success":  True
   "message":  "Question successfuly deleted
   }
  ```

### POST /questions/create

- General:

  - Creates a new question using the submitted question, answer, difficulty, and category. Returns success message.

- Sample Response:
  ` { "success": True "message": "Question successfuly deleted }`

### POST /questions/create

- General:

  - Returns a list of questions based on the submitted search keyword, and total questions

- Sample Request:

```
{
		"seachTerm":"What"
}
```

- Sample Response:

```
{
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        }
    ],
    "totalQuestions": 18
}
```

### POST /quizzes

- General:
  - Allows users to play the quiz game.
  - Uses JSON request parameters of category and previous questions.
  - Returns JSON object with random question not among previous questions.
- Response

```
{
    "question": {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
    },
    "success": true
}
```
