import sqlite3
from threading import Lock

lock = Lock()

class Database:
  def __init__(self, db_file):
    self.connection = sqlite3.connect(db_file, check_same_thread=False)
    self.cursor = self.connection.cursor()

  def user_exist(self, user_id):
    with self.connection:
      try:
        lock.acquire(True)
        res = self.cursor.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""").fetchall()
        return bool(len(res))
      finally:
        lock.release()

  def add_user(self, user_id):
    with self.connection:
      try:
        lock.acquire(True)
        self.cursor.execute(f"""INSERT INTO users (id) VALUES ('{user_id}')""")
      finally:
        lock.release()

  def user_info(self, user_id):
    with self.connection:
      try:
        lock.acquire(True)
        res = self.cursor.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""").fetchone()
        return res
      finally:
        lock.release()

  def all_users(self):
    with self.connection:
      try:
        lock.acquire(True)
        res = self.cursor.execute(f"""SELECT * FROM users""").fetchall()
        return res
      finally:
        lock.release()

  def edit_user(self, user_id, step=None, temp=None, sub_temp=None, balance=None, opponent=None, status=None, in_game=None):
    var = []
    if step != None:
      var.append(f"step = '{step}'")
    if temp != None:
      var.append(f"temp = '{temp}'")
    if sub_temp != None:
      var.append(f"sub_temp = '{sub_temp}'")
    if balance != None:
      var.append(f"balance = '{balance}'")
    if opponent != None:
      var.append(f"opponent = '{opponent}'")
    if status != None:
      var.append(f"status = '{status}'")
    if in_game != None:
      var.append(f"in_game = '{in_game}'")
    with self.connection:
      try:
        lock.acquire(True)
        self.cursor.execute(f"""UPDATE users SET {','.join(var)} WHERE id = '{user_id}'""")
      finally:
        lock.release()

  def create_game_crosszero(self, creator, player, step):
    with self.connection:
      try:
        lock.acquire(True)
        self.cursor.execute(f"""INSERT INTO games_cross-zero (creator, player, step) VALUES ('{creator}', '{player}', '{step}')""")
      finally:
        lock.release()

  def cz_info(self, creator):
    with self.connection:
      try:
        lock.acquire(True)
        res = self.cursor.execute(f"""SELECT * FROM games_cross-zero WHERE creator = '{creator}'""").fetchone()
        return res
      finally:
        lock.release()