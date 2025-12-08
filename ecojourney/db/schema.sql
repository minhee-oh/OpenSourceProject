-- User (사용자) 테이블
CREATE TABLE IF NOT EXISTS users (
    student_id TEXT PRIMARY KEY,                 -- 학번 (로그인 ID)
    password_hash TEXT NOT NULL,                -- 비밀번호 해시
    college TEXT NOT NULL,                      -- 소속 단과대 (예: 'Engineering')
    current_points INTEGER NOT NULL DEFAULT 0,  -- 현재 보유 포인트 (기본값: 0)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- 가입일
);
