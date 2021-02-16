import React, { useState } from "react";
import { Alert, Input } from "antd";
import { useHistory } from "react-router-dom";
import "./search.scss";

const { Search } = Input;

function Searchbar(props) {
  const history = useHistory();
  const [error, setError] = useState(false);

  const onSearch = (query) => {
    if (query.length > 0) {
      setError(false);
      history.push("/search/?query=" + query);
    } else {
      setError(true);
    }
  };

  return (
    <>
      <Search
        className="inner-search"
        enterButton="Search"
        placeholder={props.placeholder}
        onSearch={onSearch}
        size="large"
        defaultValue={props.inputValue}
      />
      {error && (
        <Alert message="Please type 1 or more characters" type="error" />
      )}
    </>
  );
}

export default Searchbar;
