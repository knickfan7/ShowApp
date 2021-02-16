import React, { useState, useEffect } from "react";
import WatchListAPI from "../../api/watchlistapi";
import WatchlistForm from "../forms/watchlistform";
import { Button, Tabs, Table } from "antd";
import "./watchlist.scss";

const { TabPane } = Tabs;

function WatchList() {
  const [watchlist, setList] = useState([]);

  const columns = [
    {
      title: "Image",
      dataIndex: "img",
      render: (img, title) => <img src={img} alt={title} />,
    },
    {
      title: "Title",
      dataIndex: "title",
      sorter: {
        compare: (a, b) => a.show - b.show,
        multiple: 4,
      },
    },
    {
      title: "Status",
      dataIndex: "status",
      sorter: {
        compare: (a, b) => a.status - b.status,
        multiple: 3,
      },
    },
    {
      title: "Rating",
      dataIndex: "rating",
      sorter: {
        compare: (a, b) => a.rating - b.rating,
        multiple: 2,
      },
    },
    {
      title: "Date Added",
      dataIndex: "created_dt",
      sorter: {
        compare: (a, b) => a.created_df - b.created_dt,
        multiple: 1,
      },
    },
    {
      title: "Edit",
      dataIndex: "edit",
      render: (text, record, index) => (
        <>
          <EditModal show={record} setList={setList}/>
        </>
      ),
    },
  ];

  useEffect(() => {
    WatchListAPI.retrieveAll(function (response) {
      setList(response.data);
    });
  }, []);

  return (
    <div className="watchlist-container">
      <Tabs defaultActiveKey="all">
        <TabPane tab="All Movies and Shows" key="all">
          <ShowLists watchlist={watchlist} columns={columns} />
        </TabPane>
        <TabPane tab="Currently Watching" key="Currently Watching">
          <ShowLists
            watchlist={watchlist.filter(
              (show) => show.status === "Currently Watching"
            )}
            columns={columns}
          />
        </TabPane>
        <TabPane tab="Completed" key="Completed">
          <ShowLists
            watchlist={watchlist.filter((show) => show.status === "Completed")}
            columns={columns}
          />
        </TabPane>
        <TabPane tab="On Hold" key="On Hold">
          <ShowLists
            watchlist={watchlist.filter((show) => show.status === "On Hold")}
            columns={columns}
          />
        </TabPane>
        <TabPane tab="Dropped" key="Dropped">
          <ShowLists
            watchlist={watchlist.filter((show) => show.status === "Dropped")}
            columns={columns}
          />
        </TabPane>
        <TabPane tab="Plan to Watch" key="Plan to Watch">
          <ShowLists
            watchlist={watchlist.filter(
              (show) => show.status === "Plan to Watch"
            )}
            columns={columns}
          />
        </TabPane>
      </Tabs>
    </div>
  );
}

function ShowLists(props) {
  return (
    <Table
      columns={props.columns}
      dataSource={props.watchlist}
      rowKey={record => record.show_id}
    />
  );
}

function EditModal(props) {
  const [modalVisible, setModalVisible] = useState(false);

  const showModal = () => {
    setModalVisible(true);
  };

  return (
    <>
      <Button type="primary" onClick={showModal}>
        Edit
      </Button>
      {props.show && (
        <WatchlistForm
          caller={"edit"}
          id={props.show.show_id}
          modalVisible={modalVisible}
          setModalVisible={setModalVisible}
          show={props.show}
          setList={props.setList}
          title={props.show.title}
        />
      )}
    </>
  );
}

export default WatchList;
