import React, { useState, useEffect } from "react";
import { Button, Card, Checkbox, Form, Input, Typography } from "antd";
import { EyeInvisibleOutlined, EyeTwoTone } from "@ant-design/icons";
import UserAPI from "../../api/authapi";
import { useStore } from "../../util/store/mycontext";
import { useHistory } from "react-router-dom";
import AsyncStorage from "@react-native-async-storage/async-storage";
import "./forms.scss";

const { Title } = Typography;

function Signin() {
  const [form] = Form.useForm();
  const [username, setUser] = useState("");
  const [password, setPass] = useState("");
  const [rememberMe, setRemember] = useState(true);

  const userStore = useStore().userStore;
  const history = useHistory();
  // TODO if user is logged in and goes in this page, redirect to home with message already logged in
  useEffect(() => {
    const checkInfo = async () => {
      const userObj = await AsyncStorage.getItem("@user");
      const token = await AsyncStorage.getItem("@token");

      const user = JSON.parse(userObj);
      if (user !== null && token !== null && user["rememberMe"] === true) {
        userStore.setRememberState(user.user.username, token);
        history.push("/");
      }
    };

    checkInfo();
    // eslint-disable-next-line
  }, [userStore]);
  const handleLogin = () => {
    UserAPI.login(username, password, function (response) {
      if (response !== 400) {
        userStore.setLoginState(response.user, response.token, rememberMe);
        history.push("/");
      }
      // TODO Redirect to previous page if none exist then redirect to home.
    });
  };

  const handleRedirect = () => {
    history.push("/signup/");
  };

  const handleRemember = () => {
    setRemember(!rememberMe);
  };

  return (
    <Card className="form">
      <Form layout={"vertical"} form={form}>
        <Title level={3}>Sign In</Title>
        <Form.Item label="Username">
          <Input
            placeholder="Your username"
            value={username}
            onChange={(e) => setUser(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Password">
          <Input.Password
            placeholder="Your password"
            value={password}
            iconRender={(visible) =>
              visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />
            }
            onChange={(e) => setPass(e.target.value)}
          />
        </Form.Item>
        <Form.Item>
          <Checkbox checked={rememberMe} onChange={handleRemember}>
            Remember Me
          </Checkbox>
        </Form.Item>
        <Form.Item>
          <Button className="form-btn submit" onClick={handleLogin}>
            Sign In
          </Button>
          <Button className="form-btn forgot-pass" ghost>
            Forgot your password?
          </Button>
          <Button className="form-btn submit redirect" onClick={handleRedirect}>
            Sign Up
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}

export default Signin;
