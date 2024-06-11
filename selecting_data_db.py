from connection_bd import connect


def get_list_device_variation(cur):
    '''Получаем список всех device_variation из БД'''

    cur.execute('SELECT * FROM devices_variations;')
    rows = cur.fetchall()
    word_list = []
    for row in rows:
        word_list.append(row[2])

    return word_list


def get_device_name(cursor, device_variation):
    '''Получаем более обобщённое название устройства'''

    # Для MYSQL
    # query = '''SELECT DISTINCT dv.device_name
    #         FROM devices_variations dv
    #         WHERE dv.device_variation = %s'''

    query = '''SELECT DISTINCT dv.device_name
                FROM devices_variations dv
                WHERE dv.device_variation = ?'''

    cursor.execute(query, (device_variation,))
    device_name = cursor.fetchone()[0]

    return device_name


def get_device_type(cursor, device_name):
    '''Получаем тип устройства'''

    # Для MYSQL
    # query = ('''
    #     SELECT DISTINCT d.device_type
    #     FROM devices d
    #     WHERE d.device_name = %s;''')
    # cursor.execute(query, (device_name,))
    # device_type = cursor.fetchone()[0]

    query = ('''    
        SELECT DISTINCT d.device_type
        FROM devices d
        WHERE d.device_name = ?;''')
    cursor.execute(query, (device_name,))
    device_type = cursor.fetchone()[0]

    return device_type


def get_sp_number(cursor, device_name):
    '''Получаем все названия СП для данного устройства'''

    # Для MYSQL
    # query = ('''
    #         SELECT sp_number
    #         FROM sp_devices
    #         WHERE device_name = %s;''')
    # cursor.execute(query, (device_name,))
    # all_sp_number = [i[0] for i in cursor.fetchall()]

    query = ('''    
            SELECT sp_number
            FROM sp_devices
            WHERE device_name = ?;''')
    cursor.execute(query, (device_name,))
    all_sp_number = [i[0] for i in cursor.fetchall()]

    return all_sp_number


def get_sp_description(cursor, sp_number):
    '''Получаем описание СП по его номеру'''

    # Для MYSQL
    # query = ('''
    #             SELECT sp_description
    #             FROM sp_with_description
    #             WHERE sp_number = %s;''')
    # cursor.execute(query, (sp_number,))
    # sp_description = cursor.fetchone()[0]

    query = ('''    
                SELECT sp_description
                FROM sp_with_description
                WHERE sp_number = ?;''')
    cursor.execute(query, (sp_number,))
    sp_description = cursor.fetchone()[0]

    return sp_description


def get_sp_protection(cursor, sp_number):
    '''Получаем меры защиты и их описание по номеру СП'''

    # Для MYSQL
    # query = ('''
    #             SELECT DISTINCT protection_method, protection_realize
    #             FROM sp_protection
    #             WHERE sp_number = %s;''')
    # cursor.execute(query, (sp_number,))
    # all_protections = cursor.fetchall()

    query = ('''    
                SELECT DISTINCT protection_method, protection_realize
                FROM sp_protection
                WHERE sp_number = ?;''')
    cursor.execute(query, (sp_number,))
    all_protections = cursor.fetchall()

    return all_protections


def get_sp_ubi(cursor, sp_number):
    '''Получение по СП номера УБИ'''

    # Для MYSQL
    # query = ('''
    #             SELECT possible_threats
    #             FROM sp_ubi
    #             WHERE sp_number = %s;''')
    # cursor.execute(query, (sp_number,))
    # all_possible_threats = [i[0] for i in cursor.fetchall()]

    query = ('''    
                SELECT possible_threats
                FROM sp_ubi
                WHERE sp_number = ?;''')
    cursor.execute(query, (sp_number,))
    all_possible_threats = [i[0] for i in cursor.fetchall()]

    return all_possible_threats


def get_threat_with_description(cursor, possible_threats):
    '''Получение описания УБИ по его номеру'''

    # Для MYSQL
    # query = ('''
    #                 SELECT threat_description
    #                 FROM threat_with_description
    #                 WHERE possible_threats = %s;''')
    # cursor.execute(query, (possible_threats,))
    # threat_description = cursor.fetchone()[0]

    query = ('''    
                        SELECT threat_description
                        FROM threat_with_description
                        WHERE possible_threats = ?;''')
    cursor.execute(query, (possible_threats,))
    threat_description = cursor.fetchone()[0]

    return threat_description

# lst = ['Принтер', 'Микрофон', 'Жесткий диск', 'Микрофон']
#
# con, cur = connect()
# for i in lst:
#     try:
#         name = get_device_name(cur, i)
#         d_type = get_device_type(cur, name)
#         all_sp = get_sp_number(cur, name)
#         print(f'{i} - {name} - {d_type} - {all_sp}')
#         print(get_sp_description(cur, 'СП.2.8'))
#         print(get_sp_protection(cur, 'СП.2.8'))
#         print(get_sp_ubi(cur, 'СП.2.7'))
#         print(get_threat_with_description(cur, 'УБИ.1'))
#
#     except TypeError as err:
#         print(f'Устройство {i} не найдено')
