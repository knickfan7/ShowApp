/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect, useState } from "react";
import TMDBAPI from "../../api/tmdbapi";
import Search from "../common/search";
import { Button, Card, Col, Pagination, Row, Typography } from "antd";
import { useHistory } from "react-router-dom";
import NAImg from "../../util/imgs/na.png";
import "./results.scss";

const { Title } = Typography;

function Results(props) {
  const [results, setResults] = useState([]);
  const [filter, setFilter] = useState("none");

  useEffect(() => {
    TMDBAPI.search(props.query, function (response) {
      if (response.status === 200) {
        setResults(response.data);
      }
    });
  }, [props.query]);

  return (
    <div className="results">
      <Search inputValue={props.query} />
      <Title level={4}>Search Results for "{props.query}"</Title>

      <Row>
        <Col span={8}>
          <Filter filter={filter} setFilter={setFilter} results={results} />
        </Col>
        <Col span={12}>
          {results.length !== 0 ? (
            <View
              query={props.query}
              results={results.filter((show) => show.type !== filter)}
            />
          ) : (
            <NoResults query={props.query} />
          )}
        </Col>
      </Row>
    </div>
  );
}

function Filter(props) {
  const handleClick = (filter: string) => {
    props.setFilter(filter);
  };

  return (
    <Card title="Filter" className="filter">
      <Button className="filter-btn" onClick={() => handleClick("none")}>
        <h2>All</h2>
        <h3>{props.results.length}</h3>
      </Button>
      <Button className="filter-btn" onClick={() => handleClick("tv")}>
        <h2>Movies</h2>
        <h3>{props.results.filter((show) => show.type === "movie").length}</h3>
      </Button>
      <Button className="filter-btn" onClick={() => handleClick("movie")}>
        <h2>TV Shows</h2>
        <h3>{props.results.filter((show) => show.type === "tv").length}</h3>
      </Button>
    </Card>
  );
}

function View(props) {
  const [min, setMin] = useState(0);
  const [max, setMax] = useState(20);
  const history = useHistory();

  const handleChange = (value: number) => {
    setMin((value - 1) * 20);
    setMax(value * 20);
  };

  const handleClick = (id: number, title: string, media_type: string) => {
    history.push("/" + media_type + "/" + id + "/" + title);
  };

  return (
    <div className="pagination">
      {props.results &&
        props.results.slice(min, max).map((show) => (
          <Card key={show.id}>
            <Row>
              <Col span={6}>
                {show.img !== null ? (
                  <img
                    src={show.img}
                    alt={show.title}
                    onClick={() => handleClick(show.id, show.title, show.type)}
                  />
                ) : (
                  <img
                    src={NAImg}
                    alt={show.title}
                    onClick={() => handleClick(show.id, show.title, show.type)}
                  />
                )}
              </Col>
              <Col span={16}>
                <a onClick={() => handleClick(show.id, show.title, show.type)}>
                  {show.title}
                </a>
                <h4>
                  {show.type === "movie" ? show.type : show.type + " show"}
                </h4>
              </Col>
            </Row>
          </Card>
        ))}

      <Pagination
        defaultCurrent={1}
        total={props.results.length}
        defaultPageSize={20}
        onChange={handleChange}
      />
    </div>
  );
}

function NoResults(props) {
  return (
    <div className="no-results">
      <h2>
        Your Search result "<strong>{props.query}</strong>" did not yield any
        results.
      </h2>
      <h3>Suggestions.</h3>
      <ul>
        <li>Make sure all words are spelled correctly.</li>
        <li>Try alternative name(s)</li>
      </ul>
    </div>
  );
}

export default Results;
