import sqlite3
import discord


def read_roster(channel_id):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for status read")

        c.execute('select * from signup where channel_id=? order by role desc',
                  [channel_id])

        records = c.fetchall()

        print("Total rows are:  ", len(records))
        myEmbed = discord.Embed(title="Roster", value='🧾')
        if len(records) == 0:
            myEmbed.add_field(name='Username', value="None", inline=True)
            myEmbed.add_field(name='Roles', value="None", inline=True)
            myEmbed.add_field(name='Messages', value="None", inline=True)
        if len(records) > 0:
            names = ''
            roles = ''
            messages = ''
            row = ''
            slug = ''
            tank_enrolled_count = query_role_count(channel_id, 'TANK')
            tank_limit_count = query_limit_count(channel_id, 'TANK')
            healer_enrolled_count = query_role_count(channel_id, 'HEALER')
            healer_limit_count = query_limit_count(channel_id, 'HEALER')
            dps_enrolled_count = query_role_count(channel_id, 'DPS')
            dps_limit_count = query_limit_count(channel_id, 'DPS')
            alt_enrolled_count = query_role_count(channel_id, 'ALT')
            #print(tank_enrolled_count)
            #print(healer_enrolled_count)
            #print(dps_enrolled_count)
            #print(alt_enrolled_count)

            for x in records:
                row = ''
                names = x[2] + ' '
                row += names
                if x[7] == 'DPS':
                    roles = str('⚔️') + ' '
                    row += roles
                if x[7] == 'HEALER':
                    roles = str('🚑') + ' '
                    row += roles
                if x[7] == 'TANK':
                    roles = str('🛡️') + ' '
                    row += roles
                if x[7] == 'ALT':
                    roles = str('🎲') + ' '
                    row += roles
                if x[8] is None:
                    messages = '\u200b' #+ '\n '
                    row += messages +'\n'
                if x[8] is not None:
                    messages = x[8] + ' '
                    row += messages + '\n'
                slug += row
                print(x[0])
                print(x[1])
                print(x[2])
                print(x[3])
                print(x[4])
                print(x[5])
                print(x[6])
                print(x[7])
            slug += 'Role Count:' + '\n'
            slug += 'TANKS' + ' ' + str(tank_enrolled_count) + '/' + str(tank_limit_count) + '\n'
            slug += 'HEALERS' + ' ' + str(healer_enrolled_count) + '/' + str(healer_limit_count) + '\n'
            slug += 'DPS' +' ' + str(dps_enrolled_count) + '/' + str(dps_limit_count) + '\n'
            slug += 'ALTS' + ' ' + str(alt_enrolled_count)+ '\n'
            slug += 'Total Count:' + '\n'
            slug += str(tank_enrolled_count + healer_enrolled_count + dps_enrolled_count) +'/' +str(tank_limit_count+healer_limit_count+dps_limit_count) + ' '+ '+' + str(alt_enrolled_count)+ '\n'
            myEmbed.add_field(name='\u200b', value=slug, inline=False)
        c.close()
        return myEmbed
        connection.close()

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def edit_counts(channel_id, username, tank, healer, dps):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for Trial Edit")

        c.execute('SELECT owner from trials where channel =?', [channel_id])
        exists = c.fetchall()

        if exists is not None:
            print("Modify Trial Entry")
            sql_update = """update trials set TANKS=? , HEALERS=?, DPS=? where channel=?;"""
            update_tuple = [tank, healer, dps, channel_id]
            c.execute(sql_update, update_tuple)

            connection.commit()
            print("Record update successful.")

        if exists is None:
            print("No Trial to Edit")

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def event_info(channel_id, message):
    msg = str(message)
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for Event Info Edit")

        c.execute('SELECT owner from trials where channel =?', [channel_id])
        exists = c.fetchall()

        if exists is not None:
            print("Modify Trial Entry")
            update_tuple = (msg, channel_id)
            c.execute('update trials set trial_desc=? where channel =?',
                      update_tuple)

            connection.commit()
            print("Record update successful.")

        if exists is None:
            print("No Trial to Edit")

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def roster_msg(message, channel_id, username):
    msg = str(message)
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for Roster Message")
        print(channel_id)
        print(username)
        print(msg)

        c.execute('SELECT username from signup where channel =?', [channel_id])
        exists = c.fetchall()

        if exists is not None:
            print("Modify Trial Message")
            update_tuple = (msg, channel_id, username)
            c.execute(
                'update signup set message=? where channel_id =? and username=?',
                update_tuple)

            connection.commit()
            print("Record update successful.")

        if exists is None:
            print("No Trial to Edit")

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def event_time(channel_id, message):
    msg = str(message)
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for Event Info Edit")

        c.execute('SELECT owner from trials where channel =?', [channel_id])
        exists = c.fetchall()

        if exists is not None:
            print("Modify Trial Time")
            update_tuple = (msg, channel_id)
            c.execute('update trials set trial_time=? where channel =?',
                      update_tuple)

            connection.commit()
            print("Record update successful.")

        if exists is None:
            print("No Trial to Edit")

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def read_roles():
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite")

        c.execute('select * from default_roles')
        records = c.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        myEmbed = discord.Embed(title="Default Role Assignment",
                                description='☠️',
                                color=0xFF5733)
        names = ''
        roles = ''
        for x in records:
            names += x[0] + '\n'
            if x[1] == 'DPS':
                roles += '⚔️' + '\n'
            if x[1] == 'HEALER':
                roles += '🚑' + '\n'
            if x[1] == 'TANK':
                roles += '🛡️' + '\n'
            if x[1] == 'ALT':
                roles += '🎲' + '\n'
        myEmbed.add_field(name='Username', value=names, inline=True)
        myEmbed.add_field(name='Roles', value=roles, inline=True)
        c.close()
        return myEmbed
        connection.close()

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def query_role_count(channel_id, role):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for trial existing enrollments")
        query_tuple = (channel_id, role)
        sql_query = """select count(*) from signup where channel_id=? and role=?"""
        c.execute(sql_query, query_tuple)
        query_result = c.fetchone()[0]
        query_result = int(query_result)
        print(query_result)
        c.close()
        return query_result
        connection.close()

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def query_limit_count(channel_id, role):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for trial limit for role")
        print(role)
        c.execute('select * from trials where channel=?', [channel_id])
        records = c.fetchall()
        for row in records:
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
            print(row[5])
            print(row[6])
            print(row[7])
        if role == 'TANK':
            return row[5]
        if role == 'HEALER':
            return row[6]
        if role == 'DPS':
            return row[7]
        connection.close()

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def user_role(username):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for user_role")

        c.execute('select role from default_roles where username=?',
                  [username])
        return_role = c.fetchone()[0]
        print(return_role)
        c.close()
        return return_role
        connection.close()

    except connection.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def read_event(channel_id):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for trial add")
        #sql_query="""select * from trials"""
        c.execute('select * from trials where channel=?', [channel_id])
        records = c.fetchall()
        myEmbed = discord.Embed(title="Trial Information",
                                description='🎉',
                                color=0xFF5733)
        for row in records:
            # myEmbed.add_field(name="Channel ID: ", value=row[0], inline= False)
            # myEmbed.add_field(name="Channel: ", value=row[1], inline= False)
            myEmbed.add_field(name="Owner: ", value=row[2], inline=False)
            myEmbed.add_field(name="Trial Time: ", value=row[3], inline=False)
            myEmbed.add_field(name="Trial Desc: ", value=row[4], inline=False)
            # myEmbed.add_field(name="Max Tanks: ", value=row[5], inline= False)
            # myEmbed.add_field(name="Max Healers: ", value=row[6], inline= False)
            # myEmbed.add_field(name="Max DPS: ", value=row[7], inline= False)
        connection.close()
        return (myEmbed)

    except connection.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return 2

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def add_event(channel_name, channel_id, owner):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite for trial add")
        sql_query = """select * from trials where channel_id=?"""
        read_tuple = [channel_id]
        c.execute(sql_query, read_tuple)

        exists = c.fetchone()
        print(exists)
        #Use this to update an existing user with a new role.
        if exists is not None:
            print("Channel already exists.")
        #Use this to create a new trial entry
        if exists is None:
            print("No Trial Record")
            sql_insert = """INSERT INTO trials (channel_id,channel,owner) VALUES(?,?,?);"""

            data_tuple = [channel_name, channel_id, owner]
            c.execute(sql_insert, data_tuple)
            connection.commit()
            print("Trial insert successful.")
            #return 0

            connection.close()

    except connection.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return 2

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def role_assign(username, role):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite")

        c.execute('SELECT username from default_roles where username =?',
                  [username])
        exists = c.fetchone()
        #Use this to update an existing user with a new role.
        if exists is not None:
            print("Modify Existing Entry")
            sql_update = """update default_roles set role=? where username=?;"""
            update_tuple = (role, username)

            c.execute(sql_update, update_tuple)
            connection.commit()
            print("Record update successful.")
            #return 1
        #Use this to create a new user and role pairing
        if exists is None:
            print("No Entry")
            sql_insert = """INSERT INTO default_roles (username,role) VALUES(?,?);"""
            data_tuple = [username, role]
            c.execute(sql_insert, data_tuple)
            connection.commit()
            print("Record insert successful.")
            #return 0

            connection.close()

    except connection.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return 2

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def signup_data(channel_id, username, user_id, guild_id, channel, joining,
                role):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite")

        sql_exists = """SELECT signup_id from signup where channel_id =? and username=?"""
        exists_tuple = (channel_id, username)
        c.execute(sql_exists, exists_tuple)
        exists = c.fetchone()
        if exists is not None:
            return 1
        if exists is None:
            print("No Entry")
            sql_insert = """INSERT INTO signup (channel_id,username,user_id,guild_id,channel,joining,role) VALUES(?,?,?,?,?,?,?);"""
            data_tuple = (channel_id, username, user_id, guild_id, channel,
                          joining, role)
            c.execute(sql_insert, data_tuple)
            connection.commit()
            print("Record insert successful.")
            return 0

            connection.close()

    except connection.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return 2

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def delete_signup(channel_id, username, guild_id, channel):
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to SQLite")

        sql_delete = """DELETE FROM signup where channel_id=? and username=? and guild_id=? and channel=? """

        data_tuple = (channel_id, username, guild_id, channel)
        c.execute(sql_delete, data_tuple)

        connection.commit()
        print("Record deletion successful.")

        connection.close()

    except connection.Error as error:
        print("Failed to delete Python variable into sqlite table", error)

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def nuke_signup():
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to delete all events")

        sql_delete = """DELETE FROM signup"""

        c.execute(sql_delete)  #,data_tuple)

        connection.commit()
        print("Record deletion successful.")

        connection.close()

    except connection.Error as error:
        print("Failed to delete Python variable into sqlite table", error)

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


def nuke_event():
    try:
        connection = sqlite3.connect("database.db")
        c = connection.cursor()
        print("Connected to delete all events")

        sql_delete = """DELETE FROM trials"""

        c.execute(sql_delete)  #,data_tuple)

        connection.commit()
        print("Record deletion successful.")

        connection.close()

    except connection.Error as error:
        print("Failed to delete Python variable into sqlite table", error)

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")
