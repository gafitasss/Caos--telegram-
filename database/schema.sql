CREATE TABLE players (

    user_id INTEGER PRIMARY KEY,

    username TEXT,

    name TEXT NOT NULL,

    energy INTEGER DEFAULT 100,

    fragments INTEGER DEFAULT 0,

    score INTEGER DEFAULT 0,

    level INTEGER DEFAULT 1,

    experience INTEGER DEFAULT 0,

    actions INTEGER DEFAULT 0,

    wins INTEGER DEFAULT 0,

    created_at INTEGER
);


CREATE TABLE groups (

    chat_id INTEGER PRIMARY KEY,

    round INTEGER DEFAULT 0,

    event TEXT DEFAULT 'nothing',

    round_started INTEGER DEFAULT 0,

    round_ends INTEGER DEFAULT 0,

    world_energy INTEGER DEFAULT 50,

    chaos INTEGER DEFAULT 0,

    created_at INTEGER
);


CREATE TABLE group_players (

    chat_id INTEGER,

    user_id INTEGER,

    joined_at INTEGER,

    PRIMARY KEY (
        chat_id,
        user_id
    ),

    FOREIGN KEY (
        user_id
    )
    REFERENCES players(user_id),

    FOREIGN KEY (
        chat_id
    )
    REFERENCES groups(chat_id)
);


CREATE TABLE actions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    chat_id INTEGER,

    round INTEGER,

    user_id INTEGER,

    action TEXT,

    created_at INTEGER
);
