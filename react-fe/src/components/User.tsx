class User {
    username: string;
    password: string;
    name: string;
    last_name: string;
    city: string;
    access_token: string;
    birth_year: number;
    apartment_id: string;
    internal_number: number;
  
  
  
    constructor(username: string, password: string, access_token: string, name: string, last_name: string, apartment_id: string, internal_number: number, city: string, birth_year?: number,) {
  
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