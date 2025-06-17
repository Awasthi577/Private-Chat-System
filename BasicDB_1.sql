-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    identity_key_public TEXT NOT NULL,
    identity_key_private_encrypted TEXT NOT NULL
);

-- Key store
CREATE TABLE keystore (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    signed_prekey TEXT NOT NULL,
    prekeys JSONB NOT NULL,
    last_rotated_at TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT unique_user_keystore UNIQUE (user_id)
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id),
    receiver_id UUID REFERENCES users(id),
    ciphertext TEXT NOT NULL,
    ratchet_header JSONB NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Media file encryption
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id),
    receiver_id UUID REFERENCES users(id),
    encrypted_url TEXT NOT NULL,
    aes_key_encrypted TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Audit logs
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    event_type TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Indexes for foreign keys to improve performance
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_receiver_id ON messages(receiver_id);

CREATE INDEX idx_media_files_sender_id ON media_files(sender_id);
CREATE INDEX idx_media_files_receiver_id ON media_files(receiver_id);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

CREATE INDEX idx_keystore_user_id ON keystore(user_id);
