-- backend/init.sql

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(10) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tài khoản admin mẫu (hash password bằng bcrypt, ví dụ cho demo thôi)
INSERT INTO users (username, password_hash, role)
VALUES ('admin', '$2b$12$mz/zDk9tK5iMopMuUeFvQO6Dsxz/ZhHeIGCzY44ULF8zYbiv12Xwq', 'admin')
ON CONFLICT (username) DO NOTHING;
