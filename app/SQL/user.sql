use ltalk;
#drop table user;
create Table user(
	id VARCHAR(30) NOT NULL,
    pw VARCHAR(20) NOT NULL, 
    name VARCHAR(30), 
    primary key(id)
);
INSERT into testtype values('Acapellia','','Acapellia');
INSERT into testtype values('a','','a12');
INSERT into testtype values('b','','bnb');