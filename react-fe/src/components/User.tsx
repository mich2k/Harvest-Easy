class User {
    username: string;
    password: string;
    name: string;
    last_name: string;
    city: string;
    access_token: string;
    birth_year: Number;
    apartment_id: string;
    internal_number: Number;
  
  
  
    constructor(username: string, password: string, access_token: string, name: string, last_name: string, apartment_id: string, internal_number: Number, city: string, birth_year?: Number,) {
  
      this.username = username;
      this.password = password;
      this.access_token = access_token;
      this.name = name;
      this.last_name = last_name;
      this.apartment_id = apartment_id;
      this.internal_number = internal_number;
      this.city = city;
      this.birth_year = birth_year ?? 0;
  
    }
  
  }

  export default User;