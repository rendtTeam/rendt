from dbHandler import DBHandler


test = DBHandler()
# test.createNewDB("testDB")
# test.create_dropTable("create table 1testdbonrendt(id int(11) auto_increment, primary key (id));")
# test.switchDB("testDB")
# test.create_dropTable("create table testdbonold(id int(11) auto_increment, primary key (id));")
# test.create_dropTable("drop table testdbonold;")
test.executeQuery("create table testdbonnew(id int(11) auto_increment, primary key (id));", None)
test.executeQuery("create table testdbonnew2(id int(11) auto_increment, primary key (id));", None)
# test.switchDB("RendtDB")
test.endSession()
# test.deleteDB("testDB")
# test.switchDB("testDB")