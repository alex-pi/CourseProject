import React from "react";
import './results.css';

class Results extends React.Component {
    render() {
        const { data } = this.props.location;

        if (document.title != "Results") {
            document.title = "Results";
        }

        if (data == null) {
            return (
                <h1 className="error">Error, no results present!</h1>
            );
        }

        return ([
            <h1 className="listTitle">Faculty Scraper</h1>,
            <hr className="listBar"></hr>,
            <div className="list">
                {data.map(item => (<li className="listItem"><a href={item} target="_blank" className="url">{item}</a></li>))}
            </div>
        ]);
    }
}

export default Results;
