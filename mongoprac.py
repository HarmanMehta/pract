import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify, request

cluster =  MongoClient("mongodb+srv://harmanmehta26:harman26@cluster0.6nxdbyt.mongodb.net/?retryWrites=true&w=majority")
db = cluster['School']

app = Flask(__name__)

@app.route('/create', methods = ['POST'])
def create_student():
    data = request.get_json()

    if not data or 'subject' not in data:
        return 'Subject is requried',400
    
    subject = data['subject']

    subject_collection = db[subject]

    subject_collection.insert_one(data)

    return f'student details filled'

@app.route('/read', methods=['GET'])
def read_data():
    all_data = {}
    collection_names = db.list_collection_names()

    for i in collection_names:
        collection = db[i]
        documents = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's default _id
        all_data[i] = documents

    return jsonify(all_data)


@app.route('/update', methods=['PUT'])
def update_student():
    data = request.get_json()

    if not data or not all(k in data for k in ('name', 'subject', 'marks')):
        return 'name, subject, and marks are required', 400

    subject = data['subject']
    name = data['name']
    new_marks = data['marks']

    subject_collection = db[subject]

    result = subject_collection.update_one(
        {"name": name},
        {"$set": {"marks": new_marks}}
    )

    if result.matched_count == 0:
        return f"No student found with name '{name}' in subject '{subject}'", 404
    elif result.modified_count == 0:
        return f"Marks were already {new_marks} for student '{name}'", 200
    else:
        return f"Marks updated to {new_marks} for student '{name}' in subject '{subject}'", 200

@app.route('/delete', methods=['DELETE'])
def delete_student():
    data = request.get_json()

    if not data or not all(i in data for i in ('name', 'subject')):
        return 'name and subject are required', 400

    subject = data['subject']
    name = data['name']

    subject_collection = db[subject]

    result = subject_collection.delete_one({"name": name})
    print(result.deleted_count)
    if result.deleted_count == 0:
        return f"No student found with name '{name}' in subject '{subject}'", 404
    else:
        return f"Student '{name}' deleted from subject '{subject}'", 200
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = 4000)
