/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect } from "react";
import UserAPI from "../../api/authapi";
import { useHistory } from "react-router-dom";
import { Dropdown, Menu, Row, Typography } from "antd";
import { useStore } from "../../util/store/mycontext";
import { useObserver } from "mobx-react-lite";
import AsyncStorage from "@react-native-async-storage/async-storage";
import "./navbar.scss";

const { Title } = Typography;

function Navbar() {
  const history = useHistory();
  const userStore = useStore().userStore;

  useEffect(() => {
    const checkInfo = async () => {
      const userObj = await AsyncStorage.getItem("@user");
      const token = await AsyncStorage.getItem("@token");

      const user = JSON.parse(userObj);
      if (user !== null && token !== null && user["rememberMe"] === true) {
        userStore.setRememberState(user.user.username, token);
      }
    };

    checkInfo();
  }, [userStore]);

  const handleClick = (e) => {
    if (e.key === "tv" || e.key === "movies") {
      history.push("/" + e.key + "/popular");
    } else if (e.key === "home") {
      history.push("/");
    } else if (e.key === "signup") {
      history.push("/signup");
    } else if (e.key === "signin") {
      history.push("/signin");
    } else if (e.key === "lists") {
      history.push("/mylists");
    } else if (e.key === "profile") {
      history.push("/" + userStore.state.user + "/profile");
    } else if (e.key === "settings") {
      history.push("/" + userStore.state.user + "/settings");
    } else if (e.key === "logout") {
      UserAPI.logout();
      userStore.setLogoutState();
    }
  };

  const menu = (
    <Menu onClick={handleClick}>
      <Menu.Item key="profile">
        <a>My Profile</a>
      </Menu.Item>
      <Menu.Item key="settings">
        <a>Settings</a>
      </Menu.Item>
      <Menu.Item key="logout">
        <a>Logout</a>
      </Menu.Item>
    </Menu>
  );

  return useObserver(() => (
    <nav>
      <Row>
        <Menu onClick={handleClick} mode="horizontal" className="navbar">
          <Menu.Item className="left" key="home">
            <Title level={3}>MyShowLists</Title>
          </Menu.Item>
          <Menu.Item key="tv">TV</Menu.Item>
          <Menu.Item key="movies">Movies</Menu.Item>
          <Menu.Item key="lists">My Watch Lists</Menu.Item>
          {userStore.state.isAuthenticated === false ? (
            <>
              <Menu.Item key="signin" style={{ float: "right" }}>
                Sign In
              </Menu.Item>
              <Menu.Item key="signup" style={{ float: "right" }}>
                Sign Up
              </Menu.Item>
            </>
          ) : (
            <Dropdown overlay={menu} trigger={["click"]}>
              <a>{userStore.state.user}</a>
            </Dropdown>
          )}
        </Menu>
      </Row>
    </nav>
  ));
}

export default Navbar;
