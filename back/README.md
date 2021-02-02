# pocs-official-web back

Back-end of the [POCS official web](http://ipocs.org/).

## Commands

WIP

## Database schemas

```
pocs: schema
    + tables
        board: table
            + columns
                id: int(11) NN identity null
                name: varchar(128) NN
                description: varchar(2048)
                created_at: datetime NN default current_timestamp()
                board_category_pk: int(11) NN
            + indices
                board_category_fk: index (board_category_pk) type btree
            + keys
                #1: PK (id)
            + foreign-keys
                board_category_fk: foreign key (board_category_pk) -> board_category (id)
        board_category: table
            + columns
                id: int(11) NN identity null
                name: varchar(64) NN
                created_at: datetime
                parent_id: int(11)
            + indices
                parent_fk: index (parent_id) type btree
            + keys
                #1: PK (id)
            + foreign-keys
                parent_fk: foreign key (parent_id) -> board_category (id) d:set_null
        post: table
            + columns
                id: int(11) NN identity null
                title: varchar(256) NN
                content: text NN
                md_content: text NN
                plain_content: text
                preview_content: varchar(128) NN
                background_image_url: varchar(256)
                created_at: datetime NN default current_timestamp()
                modified_at: datetime NN default current_timestamp()
                board_id: int(11) NN
                author_id: int(11) NN
            + indices
                board_fk: index (board_id) type btree
                author_fk: index (author_id) type btree
            + keys
                #1: PK (id)
            + foreign-keys
                board_fk: foreign key (board_id) -> board (id)
                author_fk: foreign key (author_id) -> user (id)
        post_tag: table
            + columns
                id: int(11) NN identity null
                name: varchar(64) NN
                post_id: int(11) NN
            + indices
                post_pk: index (post_id) type btree
            + keys
                #1: PK (id)
            + foreign-keys
                post_pk: foreign key (post_id) -> post (id) d:cascade
        user: table
            + columns
                id: int(11) NN identity null
                username: varchar(32)
                password: varchar(128) NN
                name: varchar(18) NN
                email: varchar(45) NN
                generation: int(11) NN
                student_id: varchar(12) NN
                gender: varchar(6) NN
                birth: date
                phone: varchar(13)
                joined_at: date
                is_approved: tinyint(1) NN default 0
            + indices
                user_username_uindex: unique (username) type btree
                user_email_uindex: unique (email) type btree
                user_student_id_uindex: unique (student_id) type btree
            + keys
                #1: PK (id)
                user_username_uindex: AK (username)
                user_email_uindex: AK (email)
                user_student_id_uindex: AK (student_id)
```
