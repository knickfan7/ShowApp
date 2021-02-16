import React, { useEffect, useState } from "react";
import { MovieDetails, ShowDetails, Statistics, Trailer } from "./details";
import { Col, Row } from "antd";
import Overview from "./overview";
import Search from "../common/search";
import TMDBAPI from "../../api/tmdbapi";
import "./show.scss";

function Show(props) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    TMDBAPI.info(props.id, props.type, function (response) {
      if (response.status === 200) {
        setResults(response.data);
      }
    });
  }, [props.id, props.type]);

  return (
    <div className="show-container">
      <Search inputValue={props.title} />

      {results[0] && (
        <Row>
          <Col span={6}>
            {props.type === "movie" && <MovieDetails show={results[0]} />}
            {props.type === "tv" && <ShowDetails show={results[0]} />}
            <Statistics show={results[0]} />
            <Trailer show={results[0]} />
          </Col>
          <Col span={15}>
            <Overview show={results[0]} />
          </Col>
        </Row>
      )}
    </div>
  );
}

export default Show;
