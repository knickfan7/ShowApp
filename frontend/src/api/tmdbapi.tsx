import axios from "axios";

class TMDBAPI {
  static async search(query: string, callback) {
    try {
      await axios
        .get("http://127.0.0.1:8000/api/shows/?title=" + query)
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async info(id: number, type: string, callback) {
    try {
      await axios
        .get("http://127.0.0.1:8000/api/shows/info/?id=" + id + "&type=" + type)
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async get_cast(id: number, type: string, callback) {
    try {
      await axios
        .get(
          "http://127.0.0.1:8000/api/shows/get_cast/?id=" + id + "&type=" + type
        )
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async get_tv(callback) {
    try {
      await axios.get("http://127.0.0.1:8000/api/shows/get_tv/").then((res) => {
        callback(res);
      });
    } catch (error) {
      callback(error.response.status);
    }
  }

  static async get_movie(callback) {
    try {
      await axios
        .get("http://127.0.0.1:8000/api/shows/get_movie/")
        .then((res) => {
          callback(res);
        });
    } catch (error) {
      callback(error.response.status);
    }
  }
}

export default TMDBAPI;
