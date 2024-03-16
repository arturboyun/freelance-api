CREATE MIGRATION m1ro7df6w6mp7ihwduegciaszst6clgdnwntqmel4kznhy3wwehpbq
    ONTO initial
{
  CREATE TYPE default::User {
      CREATE PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY updated_at: std::datetime {
          SET default := (std::datetime_current());
      };
  };
};
