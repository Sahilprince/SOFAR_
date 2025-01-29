from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Optional
from schemas.course_schemas import Course, Subtitle, Video

class CourseService:
    def __init__(self, mongo):
        self.mongo = mongo
        self.courses_collection = self.mongo.db.courses

    def get_all_courses(self, user_role: str) -> List[Course]:
        """
        Get all courses (accessible only to admins and faculty).
        """
        if user_role not in ["admin", "faculty"]:
            raise PermissionError("Unauthorized access")

        courses = list(self.courses_collection.find())
        return [Course(**course) for course in courses]

    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get a single course by ID (accessible to everyone).
        """
        course = self.courses_collection.find_one({"_id": ObjectId(course_id)})
        if course:
            return Course(**course)
        return None

    def create_course(self, course_data: dict) -> Course:
        """
        Create a new course.
        """
        course = Course(**course_data)
        result = self.courses_collection.insert_one(course.dict())
        course.id = str(result.inserted_id)
        return course

    def update_course(self, course_id: str, course_data: dict) -> Course:
        """
        Update an existing course.
        """
        course = self.courses_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise ValueError("Course not found")

        updated_course = Course(**course_data)
        self.courses_collection.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": updated_course.dict()}
        )
        return updated_course

    def delete_course(self, course_id: str) -> bool:
        """
        Delete a course.
        """
        result = self.courses_collection.delete_one({"_id": ObjectId(course_id)})
        return result.deleted_count > 0