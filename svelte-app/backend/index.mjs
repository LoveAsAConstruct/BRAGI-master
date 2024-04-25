import express from 'express';
import bodyParser from 'body-parser';
import bcrypt from 'bcryptjs';
import cors from 'cors';
import Database from 'better-sqlite3';

const app = express();
const db = new Database('users.db');

// Set up database
const createTable = db.prepare(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
  )`);
createTable.run();

app.use(cors());
app.use(bodyParser.json());

app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);

  try {
    const insert = db.prepare('INSERT INTO users (username, password) VALUES (?, ?)');
    insert.run(username, hashedPassword);
    res.send({ status: 'ok' });
  } catch (error) {
    res.status(500).send({ status: 'error', message: 'Failed to register user' });
  }
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const query = db.prepare('SELECT * FROM users WHERE username = ?');
    const user = query.get(username);

    if (user && await bcrypt.compare(password, user.password)) {
      res.send({ status: 'ok', username });
    } else {
      res.status(401).send({ status: 'error', message: 'Invalid credentials' });
    }
  } catch (error) {
    res.status(500).send({ status: 'error', message: 'Failed to authenticate user' });
  }
});

app.listen(3001, () => console.log('Server running on http://localhost:3001'));
