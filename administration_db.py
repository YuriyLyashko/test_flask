import pymysql, re



class AdminDB:
    _HOST_DB = 'localhost'
    _USER_DB = 'root'
    _PASSWORD_DB = '123456'


    def __init__(self, table, file):
        '''
        Add the table from the previously read file and the file as attributes
        for the newly-created class AdminDB instance.
        :param table: the table from the previously read file
        :param file: incoming file
        '''
        self.table = table
        self.name_table_data = re.search(r'\w{2,}[.]', file).group(0)[:-1]


    def create_db(self, name_db):
        '''
        Creating a database
        :param name_db: database name
        '''
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB,
                                    charset = "utf8"
                                    )
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE DATABASE {} CHARACTER SET utf8 COLLATE utf8_general_ci'.format(name_db))


    def use_db(self, name_db):
        '''
        Send inquiry 'USE <database name>' to SQL
        :param name_db: database name
        '''
        self.cur.execute('USE {}'.format(name_db))


    def connect_db(self, name_db):
        '''
        Connecting to the existing database
        :param name_db: database name
        '''
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB,
                                    db=name_db,
                                    use_unicode=True,
                                    charset="utf8"
                                    )
        self.cur = self.conn.cursor()


    def create_table(self, name_table):
        '''
        Creating a table in the existing database
        :param name_table: table name
        '''
        header = str([arg + ' varchar(40) null' for arg in self.table['structure']])[1:-1].replace("'", "")
        self.cur.execute('CREATE TABLE {}(id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, {})'
                         .format(name_table, header))


    def drop_table(self, name_table):
        '''
        Droping the table
        :param name_table: table name
        '''
        self.cur.execute('DROP TABLE {}'.format(name_table))


    def write_into(self, table_name, table):
        '''
        Writing the table from the previously read file to the table in database
        :param table_name: table name in database
        :param table: table from the previously read file
        '''
        for row, row_number in zip(table['data'], range(1, len(table['data'])+1)):
            for value in table['structure']:
                if value == table['structure'][0]:
                    self.cur.execute('INSERT INTO {}({}) VALUES ("{}")'
                                     .format(table_name, value, row[value]))
                else:
                    self.cur.execute('UPDATE {} SET {} = "{}" WHERE id = {}'
                                     .format(table_name, value, row[value], row_number))
        self.conn.commit()


    def dictfetchall(self):
        "Returns all rows from a cursor as a dict"
        desc = self.cur.description
        return [dict(zip([col[0] for col in desc], row)) for row in self.cur.fetchall()]


    def read_from(self, table_name):
        self.cur.execute('SELECT * FROM  {}'.format(table_name))
        return self.dictfetchall()



    def close_connection(self):
        '''
        Close connection with database
        '''
        self.conn.close()