/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState, useEffect } from "react";
import { Avatar, Button, Card, Col, Row, Tabs, Typography } from "antd";
import { useStore } from "../../util/store/mycontext";
import { useHistory } from "react-router-dom";
import WatchlistForm from "../forms/watchlistform";
import TMDBAPI from "../../api/tmdbapi";
import NAImg from "../../util/imgs/na.png";

const { TabPane } = Tabs;
const { Paragraph, Title } = Typography;

function Overview(props) {
  const [key, setKey] = useState("details");

  const handleKey = (key: string) => {
    setKey(key);
  };

  let title = "";
  if (props.show.type === "movie") {
    title = props.show
      ? props.show.title + " (" + props.show.release_date.substring(0, 4) + ")"
      : "";
  } else {
    title = props.show
      ? props.show.title + " (" + props.show.first_air.substring(0, 4) + ")"
      : "";
  }

  return (
    <>
      {props.show && (
        <Card title={title} className="overview">
          <Tabs activeKey={key} onChange={handleKey}>
            <TabPane tab="Details" key="details">
              <DetailsTab show={props.show} title={title} />
              <CastCard cast={props.show.cast} setKey={setKey} />
            </TabPane>
            <TabPane tab="Cast" key="cast">
              <FullCast id={props.show.id} type={props.show.type} />
            </TabPane>
            <TabPane tab="Recommendations" key="recommendations">
              <Recommendations
                recommendations={props.show.recommendations}
                type={props.show.type}
              />
            </TabPane>
          </Tabs>
        </Card>
      )}
    </>
  );
}

function DetailsTab(props) {
  const [modalVisible, setModalVisible] = useState(false);

  const userStore = useStore().userStore;

  // TODO only show modal if user is authenticated otherwise redirect user
  const showModal = () => {
    if (userStore.state.isAuthenticated) {
      setModalVisible(true);
    } else {
      console.log("Todo");
    }
  };

  return (
    <div className="details-tab">
      {props.show && (
        <>
          <Row>
            <Col span={8}>
              {props.show.img !== null ? (
                <img src={props.show.img} alt={props.show.title} />
              ) : (
                <img src={NAImg} alt={props.show.title} />
              )}
              <Button onClick={showModal} className="add-btn">
                Add To List
              </Button>
              <WatchlistForm
                id={props.show.id}
                modalVisible={modalVisible}
                setModalVisible={setModalVisible}
                show={props.show}
                title={props.title}
              />
            </Col>
            <Col span={16}>
              <RatingHeader show={props.show} />
              <strong>Genres:</strong> {props.show.genres}
            </Col>
          </Row>
        </>
      )}
    </div>
  );
}

function RatingHeader(props) {
  const [ellipsis, setEllipsis] = useState(true);
  const [ellipsisText, setText] = useState("more");

  const handleEllipsis = () => {
    if (ellipsis === false) {
      setText("more");
    } else {
      setText("less");
    }
    setEllipsis(!ellipsis);
  };

  return (
    <>
      {props.show && (
        <>
          <div className="ratings">
            <Avatar shape={"square"} size={64} icon={props.show.rating} />
            <span>TMDB rating from {props.show.vote} votes</span>
            {props.show.imdb && (
              <div className="imdb">
                <Avatar
                  shape={"square"}
                  size={64}
                  icon={props.show.imdb.imdb_rating}
                />
                <span>IMDB rating from {props.show.imdb.votes} votes</span>
              </div>
            )}
          </div>

          <Title level={4}>Synopsis</Title>
          <hr />
          <p>{props.show.overview}</p>
          <p>- (Source: TMDB)</p>

          {props.show.imdb && props.show.imdb.synopsis && (
            <>
              <Paragraph ellipsis={ellipsis}>
                {props.show.imdb.synopsis}
              </Paragraph>
              <a onClick={handleEllipsis}>{ellipsisText}</a>
              <p>- (Source: IMDB Synopsis)</p>
            </>
          )}
        </>
      )}
    </>
  );
}

function CastCard(props) {
  const setKey = () => {
    props.setKey("cast");
  };

  return (
    <Card title="Cast & Credit" className="overview-additional">
      <Row>
        {props.cast &&
          props.cast.map((cast) => (
            <Col span={8} key={cast["name"]}>
              {cast["img"] !== null ? (
                <img src={cast["img"]} alt={cast["name"]} />
              ) : (
                <img src={NAImg} alt={cast["name"]} />
              )}

              <div className="cast-info">
                <span>
                  <a>{cast["name"]}</a>
                  <span>{cast["character"]}</span>
                </span>
              </div>
            </Col>
          ))}
      </Row>
      <hr />
      <a onClick={setKey} style={{ textAlign: "center" }}>
        View All
      </a>
    </Card>
  );
}

function FullCast(props) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    TMDBAPI.get_cast(props.id, props.type, function (response) {
      if (response.status === 200) {
        setResults(response.data);
      }
    });
  }, [props.id, props.type]);

  return (
    <Card title="Cast & Credit" className="overview-additional tabs">
      <Row>
        {results &&
          results.map((cast) => (
            <Col span={6}>
              <img src={cast["img"]} alt="n/a" />
              <div className="cast-member-info">
                <span>
                  <a>{cast["name"]}</a>
                  <p>{cast["character"]}</p>
                </span>
              </div>
            </Col>
          ))}
      </Row>
    </Card>
  );
}

function Recommendations(props) {
  const history = useHistory();

  const handleClick = (id, media_type, title) => {
    history.push("/" + media_type + "/" + id + "/" + title);
  };

  return (
    <Card title="Recommendations" className="overview-additional tabs">
      <Row>
        {props.recommendations &&
          props.recommendations.map((show) => (
            <>
              <Col span={4}>
                {show["img"] !== null ? (
                  <img src={show["img"]} alt={show.title} />
                ) : (
                  <img src={NAImg} alt={show.title} />
                )}
              </Col>
              <Col span={20}>
                <a onClick={() => handleClick(show.id, props.type, show.title)}>
                  {show.title}
                </a>
                <p>{show.overview}</p>
              </Col>
            </>
          ))}
      </Row>
    </Card>
  );
}

export default Overview;
