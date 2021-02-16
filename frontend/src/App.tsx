import React from "react";
import Home from "./components/home/home";
import Navbar from "./components/navbar/navbar";
import Page from "./components/page/page";
import Results from "./components/results/results";
import Show from "./components/show/show";
import Signup from "./components/forms/signup";
import Signin from "./components/forms/signin";
import WatchList from "./components/watchlists/watchlist";
import { Route, Switch } from "react-router-dom";
import { withRouter } from "react-router";

const queryString = require("query-string");

function App(props) {
  const Search = ({ match }) => {
    const parsed = queryString.parse(props.location.search);
    const stringified = queryString.stringify(parsed);
    props.location.search = stringified;

    return (
      <>
        {match.isExact && <Results query={parsed.query} />}
        <Switch>
          <Route
            path={`${match.path}` + props.location.search}
            render={() => <Results query={parsed.query} />}
          />
        </Switch>
      </>
    );
  };

  const ShowInfo = ({ match }) => {
    return (
      <>
        {match.isExact && (
          <Show
            id={match.params.id}
            type={match.params.media_type}
            title={match.params.title}
          />
        )}
      </>
    );
  };

  const Pages = ({ match }) => {
    return (
      <>
        {match.isExact && (
          <Page type={match.params.type} filter={match.params.filter} />
        )}
      </>
    );
  };

  return (
    <>
      <Navbar />
      <Switch>
        <Route path={["/mylists/"]} component={WatchList} />
        <Route path={["/search/"]} component={Search} />
        <Route path={["/:user/profile/"]} component={Profile} />
        <Route path={["/:user/settings/"]} component={Settings} />
        <Route path={["/:media_type/:id/:title"]} component={ShowInfo} />
        <Route path={["/:type/:filter"]} component={Pages} />
        <Route path={["/signin"]} component={Signin} />
        <Route path={["/signup"]} component={Signup} />
        <Route path={["/home", "/"]} component={Home} />
      </Switch>
    </>
  );
}

function Profile() {
  return <div>Profile</div>;
}

function Settings() {
  return <div>Settings</div>
}

export default withRouter(App);
