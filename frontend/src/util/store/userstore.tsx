import AsyncStorage from "@react-native-async-storage/async-storage";

export function createUserStore() {
  const setToken = async (user, token) => {
    try {
      await AsyncStorage.setItem("@token", token);
      await AsyncStorage.setItem("@user", JSON.stringify(user));
    } catch (e) {
      // saving error
    }
  };

  const getToken = async () => {
    try {
      const value = await AsyncStorage.getItem("@token");
      if (value !== null) {
        return value;
      }
    } catch (e) {}
  };

  const removeToken = async () => {
    try {
      await AsyncStorage.removeItem("@token");
      await AsyncStorage.removeItem("@user");
    } catch (e) {
      // remove error
    }
  };

  return {
    state: {
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: getToken(),
    },

    setState(state: Object) {
      this.state = state;
    },

    logoutState: {
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: null,
    },

    setLogoutState() {
      removeToken();
      let logoutState = {
        isLoading: false,
        isAuthenticated: false,
        user: null,
        token: null,
      };
      this.state = logoutState;
    },

    loginFail: {
      isAuthenticated: false,
      user: null,
      token: null,
    },

    loginSuccess: {
      isLoading: false,
      isAuthenticated: false,
      user: null,
      token: localStorage.getItem("token"),
    },

    setLoginState(user, token, rememberMe) {
      
      let storageObj = {
        user: user,
        rememberMe: rememberMe
      };

      setToken(storageObj, token);
      console.log(rememberMe);

      let loginState = {
        isLoading: false,
        isAuthenticated: true,
        user: user.username,
        token: token,
      };
      this.state = loginState;
    },

    setRememberState(user, token) {
      let loginState = {
        isLoading: false,
        isAuthenticated: true,
        user: user,
        token: token,
      }
      this.state = loginState;
    }
  };
}
