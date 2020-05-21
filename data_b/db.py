import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('/my_space/codes/Python/karmabot/data_b/karma.db') as conn:
            #conn.execute("PRAGMA foreign_keys = 1")
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()


    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS karma_table')

    c.execute('''
        CREATE TABLE IF NOT EXISTS karma_table (
            user_id     INTEGER NOT NULL PRIMARY KEY,
            karma       INTEGER
            )
    ''')
    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_user(conn, user_id: int, karma: int):
    c = conn.cursor()
    c.execute('INSERT INTO karma_table (user_id, karma) VALUES (?, ?)',
              (user_id, karma))
    conn.commit()

@ensure_connection
def update_karma(conn, user_id: int, karma: int):
    c = conn.cursor()
    c.execute('UPDATE karma_table SET karma = ? WHERE user_id = ?', (karma, user_id, ))
    conn.commit()

@ensure_connection
def get_karma(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT karma FROM karma_table WHERE user_id = ?', (user_id, ))
    (res, ) = c.fetchone()
    return res

# @ensure_connection
# def set_karma(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('SELECT karma FROM karma_table WHERE user_id = ?', (user_id, ))
#     (res, ) = c.fetchone()
#     return res

@ensure_connection
def isCreate(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT user_id FROM karma_table WHERE user_id = ?', (user_id, ))
    res = c.fetchone()
    if res:
        return True
        #print('res is present')
    else:
        return False
        #print('res is not present')



# @ensure_connection
# def del_shop(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('DELETE FROM shops_table WHERE user_id = ? ', (user_id,))
#     conn.commit()
#
# @ensure_connection
# def add_good(conn, vendor_id: int, good_name: str, info: str):
#     c = conn.cursor()
#     c.execute('INSERT INTO goods_table (good_name, info, vendor_id) VALUES (?, ?, ?)',
#               (good_name, info, vendor_id))
#     conn.commit()
#
# @ensure_connection
# def del_good(conn, id: int):
#     c = conn.cursor()
#     c.execute('DELETE FROM goods_table WHERE id = ? ', (id,))
#     conn.commit()
#
#
# @ensure_connection
# def add_feedback(conn, user_id: int, text: str, rating: int, vendor_id: int):
#     c = conn.cursor()
#     c.execute('INSERT INTO feedback_table (user_id, text, rating, vendor_id) VALUES (?, ?, ?, ?)',
#               (user_id, text, rating, vendor_id))
#     conn.commit()
#
# @ensure_connection
# def del_feedback(conn, id: int):
#     c = conn.cursor()
#     c.execute('DELETE FROM feedback_table WHERE id = ? ', (id,))
#     conn.commit()
#
#
# @ensure_connection
# def get_shop_name(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('SELECT shop_name FROM shops_table WHERE user_id = ?', (user_id, ))
#     (res, ) = c.fetchone()
#     return res
#
# @ensure_connection
# def get_shop_info(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('SELECT info FROM shops_table WHERE user_id = ?', (user_id, ))
#     (res, ) = c.fetchone()
#     return res
#
# @ensure_connection
# def update_shop_info(conn, user_id: int, info: str):
#     c = conn.cursor()
#     c.execute('UPDATE shops_table SET info = ? WHERE user_id = ?', (info[4:], user_id, ))
#     conn.commit()
#
#
# @ensure_connection
# def get_shop_name_list(conn):
#     c = conn.cursor()
#     c.execute('SELECT shop_name, user_id FROM shops_table ')
#     return c.fetchall()
#
#
# @ensure_connection
# def get_shop_goods(conn, vendor_id: int):
#     c = conn.cursor()
#     c.execute('SELECT good_name FROM goods_table WHERE vendor_id = ?', (vendor_id, ))
#     res = c.fetchall()
#     return res
#
#
# @ensure_connection
# def update_good_name(conn, good_id: int, name: str):
#     c = conn.cursor()
#     c.execute('UPDATE goods_table SET good_name = ? WHERE id = ?', (name[7:], good_id, ))
#     conn.commit()
#
# @ensure_connection
# def update_good_info(conn, good_id: int, info: str):
#     c = conn.cursor()
#     c.execute('UPDATE goods_table SET info = ? WHERE id = ?', (info[7:], good_id, ))
#     conn.commit()
#
# @ensure_connection
# def update_good_price(conn, good_id: int, price: int):
#     c = conn.cursor()
#     c.execute('UPDATE goods_table SET price = ? WHERE id = ?', (int(price[7:]), good_id, ))
#     conn.commit()
#
#
# @ensure_connection
# def get_good_by_id(conn, id: int):
#     c = conn.cursor()
#     c.execute('SELECT good_name, info, price, vendor_id FROM goods_table WHERE id = ?', (id, ))
#     (res, ) = c.fetchall()
#     return res
#
# @ensure_connection
# def get_good_id(conn, vendor_id):
#     c = conn.cursor()
#     result = []
#     c.execute('SELECT id FROM goods_table WHERE vendor_id = ?', (vendor_id, ))
#     res = c.fetchall()
#     for el in res:
#         for el1 in el:
#             result.append(el1)
#     return result
#
# @ensure_connection
# def get_feedback_by_id(conn, id: int):
#     c = conn.cursor()
#     c.execute('SELECT user_id, text, rating FROM feedback_table WHERE id = ?', (id, ))
#     (res, ) = c.fetchall()
#     return res
#
# @ensure_connection
# def get_feedback_id(conn, vendor_id):
#     c = conn.cursor()
#     result = []
#     c.execute('SELECT id FROM feedback_table WHERE vendor_id = ?', (vendor_id, ))
#     res = c.fetchall()
#     for el in res:
#         for el1 in el:
#             result.append(el1)
#     return result
#
# @ensure_connection
# def get_shop_by_id(conn, id: int):
#     c = conn.cursor()
#     c.execute('SELECT shop_name, goods, info FROM shops_table WHERE user_id = ?', (id, ))
#     (res, ) = c.fetchall()
#     return res
#
# @ensure_connection
# def get_shops_id(conn):
#     c = conn.cursor()
#     result = []
#     c.execute('SELECT user_id FROM shops_table ')
#     res = c.fetchall()
#     for el in res:
#         for el1 in el:
#             result.append(el1)
#     return result
#
#
#
#
#
# @ensure_connection
# def get_shop_feedback(conn, user_id: int):
#     c = conn.cursor()
#     c.execute('SELECT feedback FROM shops_table WHERE user_id = ?', (user_id, ))
#     (res, ) = c.fetchone()
#     return res
#
# # @ensure_connection
# # def get_shop_user_id(conn, user_id):
# #     c = conn.cursor()
# #     c.execute('SELECT user_id FROM shops_table WHERE id = ?', (id, ))
# #     res = c.fetchone()
# #     return res
#
#
#
# @ensure_connection
# def add_column(conn):
#     c = conn.cursor()
#     c.execute('ALTER TABLE goods_table ADD COLUMN price INTEGER')
#     conn.commit()
#
#
# @ensure_connection
# def add_price(conn):
#     c = conn.cursor()
#     c.execute('UPDATE goods_table SET price = ? WHERE id = ?', (27, 6))
#     conn.commit()
