/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState, useEffect } from "react";
import { Col, Row, Typography } from "antd";
import TMDBAPI from "../../api/tmdbapi";
import NAImg from "../../util/imgs/na.png";
import { useHistory } from "react-router-dom";
import "./page.scss";

const { Title } = Typography;

function Page(props) {
  const [result, setResult] = useState([]);
  const [filter, setFilter] = useState("popular");

  useEffect(() => {
    if (props.type === "tv") {
      TMDBAPI.get_tv(function (response) {
        setResult(response.data);
      });
    } else if (props.type === "movies") {
      TMDBAPI.get_movie(function (response) {
        setResult(response.data);
      });
    }
    // TODO handle if user puts in wrong type other than tv/movie
  }, [props.type]);

  const handleFilter = (newFilter: string) => {
    setFilter(newFilter);
  };

  return (
    <div className="browse">
      <Row>
        <Col span={5}>
          <SideMenu type={props.type} onClick={handleFilter} />
        </Col>
        <Col span={17}>
          <DisplayList
            list={result.filter((list) => list.type === filter)[0]}
          />
        </Col>
      </Row>
    </div>
  );
}

function SideMenu(props) {
  // TODO rewrite this
  return (
    <div className="side-menu-navigation">
      {props.type === "tv" && <h1>TV Shows</h1>}
      {props.type === "movies" && <h1>Movies</h1>}
      <ul>
        <li onClick={() => props.onClick("popular")}>
          <a>Popular</a>
        </li>
        <li onClick={() => props.onClick("top-rated")}>
          <a>Top Rated</a>
        </li>
        {props.type === "tv" && (
          <li onClick={() => props.onClick("on-air")}>
            <a>On Air</a>
          </li>
        )}
        {props.type === "movies" && (
          <li onClick={() => props.onClick("now_playing")}>
            <a>Now Playing</a>
          </li>
        )}
        {props.type === "movies" && (
          <li onClick={() => props.onClick("upcoming")}>
            <a>Upcoming</a>
          </li>
        )}
      </ul>
    </div>
  );
}

function DisplayList(props) {
  const history = useHistory();

  const handleClick = (id: number, title: string, media_type: string) => {
    history.push("/" + media_type + "/" + id + "/" + title);
  };

  return (
    <>
      {props.list && props.list.list && (
        <Row>
          {props.list.list.map((show) => (
            <Col span={6} key={show.id}>
              <div className="container">
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
                <div className="bottom-right">
                  <Title level={4}>{show.title}</Title>
                </div>
              </div>
            </Col>
          ))}
        </Row>
      )}
    </>
  );
}

export default Page;
