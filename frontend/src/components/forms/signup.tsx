import React, { useEffect, useState } from "react";
import { Button, Card, Checkbox, Form, Input, Typography } from "antd";
import { EyeInvisibleOutlined, EyeTwoTone } from "@ant-design/icons";
import UserAPI from "../../api/authapi";
import { useStore } from "../../util/store/mycontext";
import { useHistory } from "react-router-dom";
import AsyncStorage from "@react-native-async-storage/async-storage";
import "./forms.scss";

const { Title } = Typography;

function Signup() {
  const [form] = Form.useForm();
  const [email, setEmail] = useState("");
  const [username, setUser] = useState("");
  const [password, setPass] = useState("");
  const userStore = useStore().userStore;
  const history = useHistory();
  // TODO Show errors for email
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

  const handleRegister = () => {
    UserAPI.register(username, email, password, function (response) {
      if (response !== 400) {
        // TODO Redirect to previous page if none exist then redirect to home.
        userStore.setLoginState(response.user, response.token);
        history.push("/");
      }
    });
  };

  const handleRedirect = () => {
    history.push("/signin/");
  };

  return (
    <Card className="form">
      <Form layout={"vertical"} form={form}>
        <Title level={3}>Sign Up</Title>
        <Form.Item label="Username:">
          <Input
            placeholder="Your username"
            value={username}
            onChange={(e) => setUser(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Email:">
          <Input
            placeholder="E.g email@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="Password:">
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
          <Checkbox>
            I agree to the nonexistent Terms of Service and Privacy Policy
          </Checkbox>
        </Form.Item>
        <Form.Item>
          <Button className="form-btn submit" onClick={handleRegister}>
            Create Account
          </Button>
          <div className="div-redirect">
            Already have a member?
            <Button
              className="form-btn redirect signin"
              onClick={handleRedirect}
            >
              Sign In
            </Button>
          </div>
        </Form.Item>
      </Form>
    </Card>
  );
}

export default Signup;
