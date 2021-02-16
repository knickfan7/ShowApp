import React from "react";
import ReactDOM from "react-dom";
import "./index.scss";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { MyShowsProvider } from "./util/store/mycontext"
import { BrowserRouter as Router } from "react-router-dom";
import "mobx-react-lite/batchingForReactDom";
import "antd/dist/antd.css";


ReactDOM.render(
  <React.StrictMode>
    <MyShowsProvider>
      <Router>
        <App />
      </Router>
    </MyShowsProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

reportWebVitals();
