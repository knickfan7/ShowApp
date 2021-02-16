import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

class WatchListAPI {
  static async retrieveAll(callback) {
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
      await axios
        .get("http://127.0.0.1:8000/api/user/watchlists/", config)
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async addShow(id, type, status, rating, comments, callback) {
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

    const body = JSON.stringify({ id, type, status, rating, comments });

    try {
      await axios
        .post("http://127.0.0.1:8000/api/add/show/", body, config)
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);

    }
  }

  static async getShow(show_id, callback) {
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
      await axios
        .get("http://127.0.0.1:8000/api/user/watchlists/get_show/?id=" + show_id, config)
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }
}

export default WatchListAPI;
