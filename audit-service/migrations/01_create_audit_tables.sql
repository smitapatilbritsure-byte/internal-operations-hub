-- Migration: 01_create_audit_tables.sql
-- Description: Create audit_logs table for tracking events from various microservices.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(50) NOT NULL, -- e.g., 'user-service', 'request-service'
    event_type VARCHAR(100) NOT NULL,  -- e.g., 'USER_CREATED', 'REQUEST_APPROVED'
    actor_id UUID,                     -- ID of the user performing the action (can be null for system actions)
    resource_id VARCHAR(255),          -- ID of the resource affected
    payload JSONB,                     -- Detailed event data (e.g., changes, context)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster search, filtering, and pagination
CREATE INDEX IF NOT EXISTS idx_audit_logs_service_name ON audit_logs(service_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_id ON audit_logs(actor_id);
