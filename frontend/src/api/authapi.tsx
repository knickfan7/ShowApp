import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

class UserAPI {
  static async login(username, password, callback) {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const body = JSON.stringify({ username, password });
    try {
      await axios
        .post("http://127.0.0.1:8000/api/auth/logins/", body, config)
        .then((res) => {
          callback(res.data);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async register(username, email, password, callback) {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const body = JSON.stringify({ username, email, password });
    try {
      await axios
        .post("http://127.0.0.1:8000/api/auth/register/", body, config)
        .then((res) => {
          callback(res.data);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async logout() {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    
    try {
      const value = await AsyncStorage.getItem("@token");
      if (value !== null) {
        config.headers["Authorization"] = "Token " + value;
      }
    } catch (e) {}
    try {
      await axios.post("http://127.0.0.1:8000/api/auth/logout/", null, config);
    } catch (error) {
      console.log(error.response.status);
    }
  }
}

export default UserAPI;
