DROP TABLE IF EXISTS "public"."wdbcms24_category";
-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS wdbcms24_category_id_seq;

-- Table Definition
CREATE TABLE "public"."wdbcms24_category" (
    "id" int4 NOT NULL DEFAULT nextval('wdbcms24_category_id_seq'::regclass),
    "name" varchar,
    PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "public"."wdbcms24_todo";
-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS wdbcms24_todo_id_seq;

-- Table Definition
CREATE TABLE "public"."wdbcms24_todo" (
    "id" int4 NOT NULL DEFAULT nextval('wdbcms24_todo_id_seq'::regclass),
    "user_id" int4 NOT NULL,
    "category_id" int4 NOT NULL,
    "title" varchar,
    "done" bool NOT NULL DEFAULT false,
    "due_date" varchar,
    CONSTRAINT "wdbcms24_todo_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."wdbcms24_category"("id") ON DELETE SET NULL ON UPDATE SET NULL,
    CONSTRAINT "wdbcms24_todo_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."wdbcms24_users"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "public"."wdbcms24_users";
-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS wdbcms24_users_id_seq;

-- Table Definition
CREATE TABLE "public"."wdbcms24_users" (
    "id" int4 NOT NULL DEFAULT nextval('wdbcms24_users_id_seq'::regclass),
    "api_key" varchar,
    PRIMARY KEY ("id")
);

