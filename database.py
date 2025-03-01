import mysql.connector
from flask import Flask, render_template, request, jsonify, redirect, session, url_for,flash
from datetime import datetime, timedelta
import pytz
import pandas as pd
from flask import send_file
from io import BytesIO
import io
from functools import wraps
import json
from collections import defaultdict
import os
from werkzeug.utils import secure_filename

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'rfid',
    'password': 'TRY/One12',
    'database': 'rfid',
    'port': 3306,  
    'charset': 'utf8mb4',  
    'ssl_disabled': True,  
}

class Database:
    def __init__(self, config=DB_CONFIG):
        self.config = config

    def connect(self):
        """Establish a connection to the database."""
        return mysql.connector.connect(**self.config)

    def fetch_data(self, query, params=None):
        """Execute a SELECT query and return fetched data."""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except mysql.connector.Error as e:
            print("MySQL Error:", e)
            return []

    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("MySQL Error:", e)

    def fetch_absentees(self):
        """Fetch students marked as absent."""
        query = """
            SELECT s.RFID, s.student_name, s.AbsenteeID
            FROM Students s
            JOIN General_Attendance ga ON s.RFID = ga.RFID
            WHERE ga.Status = 'Absent'
        """
        return self.fetch_data(query)

