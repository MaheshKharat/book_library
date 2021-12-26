# book_library

1. If you have already python installed then create viretualenv
2. Activate virtualenv
3. Then install all packages from requirements.txt
> pip install -r requirements.txt
4. Then run app.py
> python app.py
 
5. Open http://127.0.0.1:5000/api/
6. Browse that url we will see swagger documentation of apis
----------------------------------------------

I have added following routes/endpoints
1. Create/Get Book

GET, POST  /api/books
GET        /api/books/<string:book_id>

2. Create/Get Libraries

GET, POST  /api/libraries
GET        /api/libraries/<string:library_id>

3. Assign Books To The Library And Check-In/Check-Out Records

GET, POST  /api/library_book_records
GET        /api/library_book_records/find/by_library
GET        /api/library_book_records/find/by_user
GET, POST  /api/library_book_records/<string:library_book_id>/activities

4. Create/Get Users

GET, POST  /api/users



And I have added some suggestions and questions in suggestions_and_questions.txt file please check that.

Thank You.