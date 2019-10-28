CREATE TABLE p_antenna_delay
(
    refTime INTEGER,
    freq INTEGER DEFAULT 1,
    theValue TEXT,
    CONSTRAINT p_antenna_delay_reftime_freq_pk PRIMARY KEY (reftime, freq)
);
CREATE TABLE p_antenna_position
(
    refTime INTEGER,
    freq INTEGER DEFAULT 1,
    theValue TEXT,
    CONSTRAINT p_antenna_position_reftime_freq_pk PRIMARY KEY (reftime, freq)
);
CREATE TABLE p_intrument_status
(
    refTime INTEGER,
    freq INTEGER DEFAULT 1,
    theValue TEXT,
    CONSTRAINT p_intrument_status_reftime_freq_pk PRIMARY KEY (reftime, freq)
);
CREATE TABLE p_weather
(
    refTime INTEGER,
    theValue TEXT
);
CREATE TABLE t_global
(
    keyName TEXT,
    theValue TEXT,
    refTime INTEGER DEFAULT 0
);