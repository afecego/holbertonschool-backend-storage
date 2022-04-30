-- Write a SQL script that creates a trigger that resets the attribute
-- valid_email only when the email has been changed.

CREATE TRIGGER reset_valid_mail
BEFORE UPDATE ON users
FOR EACH ROW
IF OLD.email != NEW.email
THEN
SET NEW.valid_email = 0;
END IF;