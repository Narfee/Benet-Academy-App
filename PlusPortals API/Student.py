# MIT License

# Copyright (c) 2021 Nicholas Papciak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
 
from Client import Client

class Student(Client): 
    def __init__(self, school_name, email, password):
        super().__init__(school_name, email, password)
        self.grades = []

    def __str__(self):
        return f"School: {self.school_name}\nEmail: {self.email}\nPassword: {'*'*len(self.password)}"

    def check_grades(self): 
        """Returns a string representation of the grades of the student"""
        grades = self.get_grades()
        string = ""

        for marking_period in grades: 
            string += marking_period["period_name"] + ":\n"

            courses = marking_period["data"]
            for course in courses:
                string += "\t" + course["name"] + " : " + str(course["average"]) + "\n"
        return string 

    def get_grades(self):
        """
        Retrieves the grades for the current person

        Returns: 
            list[dict] = a list of marking periods and grades for that period
        """
        if self.grades == []: 
            self.grades = super().get_grades()
        return self.grades

    def refresh_grades(self):
        """Resets the grades and retrieves them again if necessary""" 
        self.grades = []
        self.grades = super().get_grades()
        return self.grades
    