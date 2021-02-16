import React from "react";
import { Card } from "antd";
import moment from "moment";
import ReactPlayer from "react-player";

function MovieDetails(props) {
  return (
    <Card title="Details" className="details">
      {props.show && (
        <ul>
          <li>
            <strong>Movie: </strong> {props.show.title}
          </li>
          <li>
            <strong>Country: </strong> {props.show.countries}
          </li>
          <li>
            <strong>Release Date: </strong>
            {moment(props.show.release_date.replace(/-/g, "/"), "Y/M/D").format(
              "MMMM D, Y"
            )}
          </li>
          <li>
            <strong>Runtime: </strong> {props.show.runtime} minutes
          </li>
          <li>
            <strong>Genres: </strong> {props.show.genres}
          </li>
          <li>
            <strong>Status: </strong> {props.show.status}
          </li>
        </ul>
      )}
    </Card>
  );
}

function ShowDetails(props) {
  return (
    <Card title="Details" className="details">
      {props.show && (
        <ul>
          <li>
            <strong>TV Show: </strong> {props.show.title}
          </li>
          <li>
            <strong>Country: </strong> {props.show.countries}
          </li>
          <li>
            <strong>Seasons: </strong> {props.show.seasons}
          </li>
          <li>
            <strong>Episodes: </strong> {props.show.num_eps}
          </li>
          <li>
            <strong>Aired: </strong>
            {moment(props.show.first_air.replace(/-/g, "/"), "Y/M/D").format(
              "MMMM D, Y"
            )}
            {" - "}
            {moment(props.show.last_air.replace(/-/g, "/"), "Y/M/D").format(
              "MMMM D, Y"
            )}
          </li>
          {props.show.next_air && (
            <li>
              <strong>Next Air: </strong>
              {props.show.next_air &&
                moment(
                  props.show.next_air["air_date"].replace(/-/g, "/"),
                  "Y/M/D"
                ).format("MMMM D, Y")}
            </li>
          )}
          <li>
            <strong>Episode Length: </strong> {props.show.ep_runtime} minutes
          </li>
          <li>
            <strong>Genres: </strong> {props.show.genres}
          </li>
          <li>
            <strong>Status: </strong> {props.show.status}
          </li>
        </ul>
      )}
    </Card>
  );
}

function Statistics(props) {
  return (
    <Card title="Statistics" className="details">
      {props.show && (
        <ul>
          <li>
            <strong>TMDB Ratings: </strong> {props.show.rating}
          </li>
          <li>
            <strong>TMDB Votes: </strong> {props.show.vote}
          </li>
          <li>
            <strong>TMDB Popularity: </strong> {props.show.popularity}
          </li>
        </ul>
      )}
    </Card>
  );
}

function Trailer(props) {
  return (
    <Card title="Trailer" className="details trailer">
      {props.show && props.show["trailer"].length > 0 ? (
        <ReactPlayer
          url={props.show["trailer"].length > 0 && props.show["trailer"][0]}
          className="player"
        />
      ) : (
        <p>No Videos Available!</p>
      )}
    </Card>
  );
}

export { MovieDetails, ShowDetails, Statistics, Trailer };
