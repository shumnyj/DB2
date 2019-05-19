import MyTables
# import psycopg2
# from psycopg2.extras import RealDictCursor, DictCursor, NamedTupleCursor
# from psycopg2 import sql
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc

url = 'postgresql+psycopg2://shumnyj:111@localhost:5432/testpost'
tables = (MyTables.Book, MyTables.Author, MyTables.Publisher)
# tables = ('books', 'authors', 'publishers')


def cast_values(values, types, fields):
    for j, val in enumerate(values):
        if val == '' or val == ' ' or val.lower() == 'null' or val.lower() == 'none':
            values[j] = None
        elif types[j] == 'integer':
            try:
                values[j] = int(values[j])
            except TypeError:
                print("invalid field value: {}".format(fields[j]))
                return None
                # alert = True
        elif types[j] == 'boolean':
            try:
                values[j] = bool(values[j])
            except TypeError:
                print("invalid field value: {}".format(fields[j]))
                return None
        else:
            values[j].strip()
                # alert = True
    return values


def table_choose():
    print('Avalible tables:')
    for i, val in enumerate(tables):
        print('{}: {};'.format(i, val.__tablename__), end=' ')
    print(' ')
    i = None
    while i is None:
        try:
            i = int(input())
        except TypeError and ValueError:
            print('Please enter valid number')
            i = None
    if i > len(tables)-1 or i < 0:
        print('Wrong value, quitting')
        return None
    else:
        return tables[i]


def db_add():
    # alert = False
    act_table = table_choose()
    if act_table is None:
        return None
    fields, types = act_table.col()
    for f in zip(fields, types):
        print("{}:{}".format(*f))

    values = input('Please, enter values\n')
    values = values.split(',')
    values = cast_values(values, types, fields)

    record = act_table(values)
    if record is not None:
        try:
            session.add(record)
            # x = session.query(act_table).filter_by(title='b243').one()
            session.commit()
        except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.ProgrammingError:
            print('Integrity error, check values')
    else:
        print('Invalid values count')


def db_update():
    act_table = table_choose()
    if act_table is None:
        return None
    fields, types = act_table.col()
    for f in zip(fields, types):
        print("{}:{}".format(*f))
    print('Choose fields to update')
    updating = input().split(',')
    for en in updating:
        en = en.strip()
        try:
            fields.index(en)
        except ValueError:
            print('One or more input fields are invalid')
            return
    print('Enter new field values in the same order')
    values = input().split(',')
    if len(updating) == len(values):
        cond = input('Enter WHERE condition\n')
        try:
            updated = session.query(act_table).filter(text(cond)).first()
        except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.ProgrammingError:
            print("Bad condition")
        if updated is not None:
            for f, v in zip(updating, values):
                setattr(updated, f, v)
            session.commit()
        else:
            session.rollback()
    else:
        print('Values count does not match required fields')


def db_remove():
    act_table = table_choose()
    if act_table is None:
        return None
    fields, types = act_table.col()
    for f in zip(fields, types):
        print("{}:{}".format(*f))
    cond = input('Enter WHERE condition\n')
    try:
        deleted = session.query(act_table).filter(text(cond)).first()
    except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.ProgrammingError:
        print("Bad condition")
    if deleted is not None:
        session.delete(deleted)
        session.commit()
    else:
        session.rollback()
        print('No such entries')


def db_search():
    try:
        mode = int(input('Select search type: 1.Range; 2.Enum; 3.Text full; 4.Text exclude;\n'))
    except ValueError:
        print('Bad input')
        return

    if mode == 1:
        act_table = table_choose()
        fields, types = act_table.col()
        for f in zip(fields, types):
            if f[1] == 'integer':
                print("{}:{}".format(*f))
        print('Enter search field')
        ff = input().strip()
        try:
            i = fields.index(ff)
            if types[i] != 'integer':
                print("Not numeric")
                return
        except ValueError:
            print('Selected field does not exist')
            return
        try:
            left = int(input('enter lower limit\n'))
            right = int(input('enter upper limit\n'))
        except ValueError:
            print('Not a number!')
            return
        cond = '{} BETWEEN {} AND {}'.format(ff, left, right)
        found = session.query(act_table).filter(text(cond)).all()
        for row in found:
            print(row)
    elif mode == 2:
        act_table = table_choose()
        fields, types = act_table.col()
        for f in zip(fields, types):
            if f[1][:7] == 'varchar':
                print("{}:{}".format(*f))
        print('Enter search field')
        ff = input().strip()
        try:
            i = fields.index(ff)
            if types[i][:7] != "varchar":
                print("Not string")
                return
        except ValueError:
            print('Selected field does not exist')
            return
        found = session.query(getattr(act_table, ff)).group_by(text(ff)).all()
        # found = session.query(MyTables.Book, MyTables.Author).join(MyTables.Author,
        #                                           and_(MyTables.Author.fname == MyTables.Book.author_fname,
        #                                                MyTables.Author.sname == MyTables.Book.author_sname))\
        #    .group_by(text(ff)).all()
        print('Avalible values:')
        for row in found:
            a = getattr(row, ff)
            print(a, end=',')
        fv = input('\nEnter value\n')
        cond = '{} = {!r}'.format(ff, fv)
        found = session.query(act_table).filter(text(cond)).all()
        for row in found:
            print(row)
    elif mode == 3:
        fv = input('Enter text search values separated by space\n')
        fv = fv.split(' ')
        quer = ''
        for v in fv:
            quer += v + ' & '
        quer = quer[:-3]
        for t in tables:
            com = ''
            act_table = t
            fields, types = act_table.col()
            for i in range(len(types)):
                if types[i][:7] == "varchar":
                    com += 'coalesce(' + fields[i] + ', \'\') || \' \' || '
            com = com[:-11]
            found = session.query(act_table).filter(func.to_tsvector('english', text(com)).
                                                    match(quer, postgresql_regconfig='english')).all()
            "com = 'SELECT * FROM ' + t + ' WHERE to_tsvector(' \
                  + com + ') @@ to_tsquery(\'english\', \'' + quer + '\')'"
            if len(found) > 0:
                print('In table ' + act_table.__tablename__)
                for row in found:
                    print(row)
    elif mode == 4:
        fv = input('Enter text search value that entries must not include\n')
        for t in tables:
            com = ''
            act_table = t
            fields, types = act_table.col()
            for i in range(len(types)):
                if types[i][:7] == "varchar":
                    com += 'coalesce(' + fields[i] + ', \'\') || \' \' || '
            com = com[:-11]
            found = session.query(act_table).filter(~func.to_tsvector('english', text(com)).
                                                    match(fv, postgresql_regconfig='english')).all()
            if len(found) > 0:
                print('In table ' + act_table.__tablename__)
                for row in found:
                    print(row)
    else:
        print('Bad input')
        return


engine = create_engine(url, echo=False)
Session = sessionmaker(bind=engine)
MyTables.Base.metadata.create_all(engine)
session = Session()
# connection = psycopg2.connect(dbname='testpost', user='shumnyj', password='111', host='localhost')
# curs = connection.cursor(cursor_factory=NamedTupleCursor)
p = False
while True:
    print('Select action:\n0: Quit; 1:Add; 2:Remove; 3:Update; 4:Search; ')
    try:
        p = int(input())
    except TypeError and ValueError:
        print('Please enter valid number')
    if p == 0:
        print('exit')
        break
    elif p == 1:
        db_add()
    elif p == 2:
        db_remove()
    elif p == 3:
        db_update()
    elif p == 4:
        db_search()
    else:
        print('Please enter valid number')
        p = None
session.close()

"""    elif p == 5:
        c = input()
        try:
            res = session.query(*tables).from_statement(text(c)).all()
            if res is not None:
                for rec in res:
                    print(rec)
        except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.ProgrammingError:
            print('Invalid command string')"""

