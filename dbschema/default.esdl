module default {
    type User {
        required name: str;
        created_at: datetime {
            default := datetime_current();
        }
        updated_at: datetime {
            default := datetime_current();
        }
    }
}
