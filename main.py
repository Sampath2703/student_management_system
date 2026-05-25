from fastapi import FastAPI
import mysql.connector

conn_obj = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="Nani@2703",
    database="api"
)

cursor_obj = conn_obj.cursor(dictionary=True) 

app = FastAPI()


@app.post("/students")
def Add_students(student_data: dict):
    name = student_data["name"]
    age = student_data["age"]
    grade = student_data["grade"]
    section = student_data["section"]
    father_name = student_data["father_name"]
    village = student_data["village"]


    query = "INSERT INTO student (name, age, grade, section, father_name, village) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (student_data["name"], student_data["age"], student_data["grade"], student_data["section"], student_data["father_name"], student_data["village"])
    cursor_obj.execute(query, values)
    conn_obj.commit()
    return {"message": "Student added successfully"}

@app.get("/get_students")
def get_students():
    query = "select * from student"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()
    return {"students": data}


@app.get("/get_single_student/{student_id}")
def get_single_student(student_id: int):            
    query = "select * from student where id = %s"
    cursor_obj.execute(query, (student_id,))
    data = cursor_obj.fetchone()
    if data:
        return {"student_data": data}
    else:
        return {"message": "Student not found"}
    
@app.put("/update_student/{student_id}")
def update_student(student_id: int, updated_student_data: dict):
    name = updated_student_data["name"]
    age = updated_student_data["age"]
    grade = updated_student_data["grade"]
    section = updated_student_data["section"]
    father_name = updated_student_data["father_name"]
    village = updated_student_data["village"]

    query = "UPDATE student SET name = %s, age = %s, grade = %s, section = %s, father_name = %s, village = %s WHERE id = %s"
    values = (name, age, grade, section, father_name, village, student_id)
    cursor_obj.execute(query, values)
    conn_obj.commit()
    return {"message": "Student updated successfully"}


@app.delete("/delete_student/{student_id}")
def delete_student(student_id: int):
    query = "DELETE FROM student WHERE id = %s"
    cursor_obj.execute(query, (student_id,))
    conn_obj.commit()
    return {"message": "Student deleted successfully"}

