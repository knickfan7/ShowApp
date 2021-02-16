import React, { useState, useEffect } from "react";
import {
  Button,
  Col,
  Dropdown,
  Input,
  Form,
  Menu,
  Modal,
  Rate,
  Row,
} from "antd";
import NAImg from "../../util/imgs/na.png";
import WatchlistAPI from "../../api/watchlistapi";
import "./forms.scss";

const { TextArea } = Input;

function WatchlistForm(props) {
  useEffect(() => {
    WatchlistAPI.getShow(props.id, function (response) {
      try {
        const data = response.data[0];
        setStatus(data["status"]);
        setRating(data["rating"]);
        setComments(data["comment"]);
      } catch {}
    });
  }, [props.id]);

  const [comments, setComments] = useState("");
  const [rating, setRating] = useState(0.0);
  const [status, setStatus] = useState("Currently Watching");

  const handleCancel = () => {
    props.setModalVisible(false);
  };

  const handleOk = () => {
    let id: number;
    if (props.caller === "edit") {
      id = props.show.show_id;
    } else {
      id = props.show.id;
    }

    WatchlistAPI.addShow(
      id,
      props.show.type,
      status,
      rating,
      comments,
      function (response) {
        try {
          props.setList(response.data);
        } catch {}
      }
    );
    props.setModalVisible(false);
  };

  // TODO Delete from watchlist
  const handleDelete = (e) => {
    console.log(e.key);
  };

  const footer = (
    <div key="key">
      <Button
        key="delete"
        onClick={handleDelete}
        danger
        style={{ float: "left" }}
      >
        Delete
      </Button>

      <Button key="cancel" onClick={handleCancel}>
        Cancel
      </Button>

      <Button key="submit" type="primary" onClick={handleOk}>
        Submit
      </Button>
    </div>
  );

  return (
    <>
      {props.show && (
        <Modal
          className="watchlist-form"
          footer={[footer]}
          onOk={handleOk}
          onCancel={handleCancel}
          title={props.title}
          visible={props.modalVisible}
        >
          <Row>
            <Col span={9}>
              {props.show.img !== null ? (
                <img src={props.show.img} alt={props.show.title} />
              ) : (
                <img src={NAImg} alt={props.show.title} />
              )}
            </Col>
            <Col span={12}>
              <AddForm
                rating={rating}
                status={status}
                setRating={setRating}
                comments={comments}
                setComments={setComments}
                setStatus={setStatus}
              />
            </Col>
          </Row>
        </Modal>
      )}
    </>
  );
}

function AddForm(props) {
  const [form] = Form.useForm();

  const handleMenuClick = (e) => {
    props.setStatus(e.key);
  };

  const handleRating = (value: number) => {
    props.setRating(value * 2);
  };

  const handleComments = (e) => {
    props.setComments(e.target.value);
  };

  const menu = (
    <Menu onClick={handleMenuClick}>
      <Menu.Item key="Currently Watching">Currently watching</Menu.Item>
      <Menu.Item key="Completed">Completed</Menu.Item>
      <Menu.Item key="Plan to Watch">Plan to watch</Menu.Item>
      <Menu.Item key="Dropped">Dropped</Menu.Item>
      <Menu.Item key="On Hold">On-Hold</Menu.Item>
    </Menu>
  );

  return (
    <>
      <Form form={form}>
        <Form.Item label="Status">
          <Dropdown
            overlay={menu}
            trigger={["click"]}
            className="watchlist-dropdown"
          >
            <Button
              className="ant-dropdown-link"
              onClick={(e) => e.preventDefault()}
            >
              {props.status}
            </Button>
          </Dropdown>
        </Form.Item>

        <Form.Item label="User Rating">
          <Rate
            allowHalf
            defaultValue={props.rating / 2}
            onChange={handleRating}
          />
          {props.rating ? (
            <span className="ant-rate-text">{[props.rating + "/10"]}</span>
          ) : (
            ""
          )}
        </Form.Item>

        <Form.Item label="Comments">
          <TextArea
            className="comments"
            defaultValue={props.comments}
            onChange={handleComments}
            rows={7}
          />
        </Form.Item>
      </Form>
    </>
  );
}

export default WatchlistForm;
