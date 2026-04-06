CREATE TABLE IF NOT EXISTS model_registry (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    version VARCHAR(64) DEFAULT 'v1',
    model_type VARCHAR(64) DEFAULT 'judge',
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluation_tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(32) DEFAULT 'pending',
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_format VARCHAR(32) DEFAULT 'json',
    duplicate_hash VARCHAR(128),
    is_desensitized BOOLEAN DEFAULT FALSE,
    error_message TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_id INTEGER REFERENCES model_registry(id)
);

CREATE TABLE IF NOT EXISTS parsed_traces (
    id SERIAL PRIMARY KEY,
    task_id INTEGER UNIQUE REFERENCES evaluation_tasks(id) ON DELETE CASCADE,
    parse_status VARCHAR(32) DEFAULT 'pending',
    node_count INTEGER DEFAULT 0,
    normalized_payload JSONB,
    tree_payload JSONB,
    timeline_payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS score_results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER UNIQUE REFERENCES evaluation_tasks(id) ON DELETE CASCADE,
    accuracy DOUBLE PRECISION DEFAULT 0,
    logic_consistency DOUBLE PRECISION DEFAULT 0,
    tool_efficiency DOUBLE PRECISION DEFAULT 0,
    safety DOUBLE PRECISION DEFAULT 0,
    total_score DOUBLE PRECISION DEFAULT 0,
    verdict VARCHAR(32) DEFAULT 'pending',
    summary TEXT DEFAULT '',
    deduction_reasons JSONB,
    chain_of_thought TEXT DEFAULT '',
    scoring_status VARCHAR(32) DEFAULT 'pending',
    judge_model VARCHAR(128) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_metrics (
    id SERIAL PRIMARY KEY,
    task_id INTEGER UNIQUE REFERENCES evaluation_tasks(id) ON DELETE CASCADE,
    processing_seconds DOUBLE PRECISION DEFAULT 0,
    token_consumption INTEGER DEFAULT 0,
    success_rate DOUBLE PRECISION DEFAULT 0,
    bad_case BOOLEAN DEFAULT FALSE,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
