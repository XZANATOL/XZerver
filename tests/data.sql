CREATE TABLE user (
	id INTEGER PRIMARY KEY,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	name TEXT NOT NULL,
	is_active BOOL,
	is_admin BOOL
);

INSERT INTO user (email, password, name, is_active, is_admin)
VALUES
	-- password: test
	('admin@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'admin', 1, 1),
	('other@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'other', 1, 1);