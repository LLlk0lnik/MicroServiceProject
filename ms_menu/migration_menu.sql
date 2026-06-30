BEGIN;

CREATE TABLE menu.alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> b0b2421b6eee

CREATE TABLE menu.positions (
    id SERIAL NOT NULL, 
    title VARCHAR NOT NULL, 
    price NUMERIC(10, 2) NOT NULL, 
    description VARCHAR, 
    category VARCHAR NOT NULL, 
    composition VARCHAR, 
    calories INTEGER, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    is_available BOOLEAN NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_menu_positions_id ON menu.positions (id);

CREATE TABLE menu.super_positions (
    id SERIAL NOT NULL, 
    title VARCHAR NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    description VARCHAR, 
    is_available BOOLEAN NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_menu_super_positions_id ON menu.super_positions (id);

CREATE TABLE super_position_items (
    super_position_id INTEGER NOT NULL, 
    position_id INTEGER NOT NULL, 
    PRIMARY KEY (super_position_id, position_id), 
    FOREIGN KEY(position_id) REFERENCES menu.positions (id), 
    FOREIGN KEY(super_position_id) REFERENCES menu.super_positions (id)
);

INSERT INTO menu.alembic_version (version_num) VALUES ('b0b2421b6eee') RETURNING menu.alembic_version.version_num;

COMMIT;

