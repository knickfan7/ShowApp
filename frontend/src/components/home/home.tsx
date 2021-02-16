import React from "react";
import Search from "../common/search";
import "./home.scss";

function Home() {
  return (
    <div className="home">
      <Search
        placeholder={"Search for a movie, tv show, ..."}
        inputValue={""}
      />
    </div>
  );
}

export default Home;
