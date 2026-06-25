import os
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'notes.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '',
                color TEXT DEFAULT '#2c2c35',
                is_pinned INTEGER DEFAULT 0,
                is_archived INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, tags, color, is_pinned, is_archived, created_at, updated_at
                FROM notes
                WHERE is_archived = 0
                ORDER BY is_pinned DESC, updated_at DESC
            ''')
            notes = [dict(row) for row in cursor.fetchall()]
        return jsonify(notes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/archived', methods=['GET'])
def get_archived_notes():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, tags, color, is_pinned, is_archived, created_at, updated_at
                FROM notes
                WHERE is_archived = 1
                ORDER BY updated_at DESC
            ''')
            notes = [dict(row) for row in cursor.fetchall()]
        return jsonify(notes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    try:
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        tags = data.get('tags', '').strip()
        color = data.get('color', '#2c2c35').strip()
        is_pinned = int(data.get('is_pinned', 0))

        if not title and not content:
            return jsonify({'error': 'Title and Content cannot both be empty.'}), 400

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notes (title, content, tags, color, is_pinned)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, tags, color, is_pinned))
            conn.commit()
            note_id = cursor.lastrowid
            
            cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
            new_note = dict(cursor.fetchone())
            
        return jsonify(new_note), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        data = request.get_json() or {}
        with get_db() as conn:
            cursor = conn.cursor()
            # Fetch existing note
            cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
            note = cursor.fetchone()
            if not note:
                return jsonify({'error': 'Note not found.'}), 404
            
            # Prepare updated values
            title = data.get('title', note['title'])
            content = data.get('content', note['content'])
            tags = data.get('tags', note['tags'])
            color = data.get('color', note['color'])
            is_pinned = data.get('is_pinned', note['is_pinned'])
            is_archived = data.get('is_archived', note['is_archived'])
            
            cursor.execute('''
                UPDATE notes
                SET title = ?, content = ?, tags = ?, color = ?, is_pinned = ?, is_archived = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, content, tags, color, is_pinned, is_archived, note_id))
            conn.commit()
            
            cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
            updated_note = dict(cursor.fetchone())
            
        return jsonify(updated_note)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
            note = cursor.fetchone()
            if not note:
                return jsonify({'error': 'Note not found.'}), 404
            
            cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
            
        return jsonify({'message': 'Note deleted successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
