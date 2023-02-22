INSERT INTO	public."role" VALUES (1,'admin','[]'), (2,'user','[]'), (3,'operator','[]');
INSERT INTO public."user" (username,full_name,email,hashed_password,disabled,role_id) VALUES
	 ('jim','Jim Holden','jim@test.ee','$2b$12$PznZt2lZGucDVkbU6jgOp.6lGplA7abllkfGSblC9fGW5ypF1VqZ6',false,2),
	 ('naomi','Naomi Nagata', 'naomi123@email.ee', '$2b$12$yzNZvwoZqnF3d2a7O19VDe911isWT90lpC8lTA96hOBTTs5e27M5i',false,2),
	 ('admin','Admin', 'admin_test@email.ee', '$2b$12$cnSW9f6.SAEzpc.soYu36Om5kdCVaTai8ZsSE.wiID6WKXmwFBESG',false,1);
