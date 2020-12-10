import React from 'react';
import './faculty_scraper.css';
import { FaSearch } from 'react-icons/fa';
import { Puff } from '@agney/react-loading';

class FacultySearchBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            url: '',
            loading: false
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.sendRequest = this.sendRequest.bind(this);
    }

    handleChange(event) {
        this.setState({ url: event.target.value });
        var urlString = String(event.target.value).replace(/\/$/, "")
        if (this.validateUrl(urlString)) {
            document.getElementById("input").setCustomValidity("Invalid URL: Make sure you are providing a valid university URL (starts with http(s):// and ends with .edu).");
            return;
        }
        document.getElementById("input").setCustomValidity("");
    }

    handleSubmit(event) {
        event.preventDefault();

        // Do nothing if already loading something.
        if (this.state.loading)
            return;

        // Want to accept only URls that end in .edu ignoring trailing /s.
        var urlString = String(this.state.url).replace(/\/$/, "")
        if (this.validateUrl(urlString)) {
            console.log("Invalid URL.");
            return;
        }
        this.setState({loading: true});

        // Send the request and start polling.
        this.sendRequest()
    }

    validateUrl(urlString) {
        return !urlString.endsWith('.edu') || !/^[a-zA-Z:\/\.]+$/.test(urlString) ||
            (!urlString.startsWith('http://www.') && !urlString.startsWith('https://www.'));
    }

    sendRequest() {
        // Send request to flask with the URL.
        const requestOptions = {
            method: 'POST',
            mode: "cors",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: this.state.url })
        };

        fetch('https://facultyscraper-heroku.herokuapp.com/', requestOptions)
            .then(response => {
                if (response.ok)
                    return response.json();
                else
                    throw new Error("Bad response!");
            })
            .then(data => {
                if (data["result"]) {
                    this.setState({ loading: false, url: "" });

                    // Don't go to results page if nothing to display.
                    if (data["urls"].length == 0) {
                        document.getElementById("input").setCustomValidity("Failed to get results! Check URL and make sure it is correct. Maybe try with/without the www.");
                    }

                    this.props.history.push({ pathname: "/results", data: data["urls"] });
                } else {
                    setTimeout(this.sendRequest, 10000);
                }
            })
            .catch((_error) => {
                this.setState({ loading: false });
                document.getElementById("input").setCustomValidity("Invalid URL! Try another variation of this URL and make sure it is accessible!");
            });
    }

    render() {
        if (document.title != "Faculty Scraper") {
            document.title = "Faculty Scraper";
        }

        return [
            <h1 className="title">Faculty Scraper</h1>,
            <form onSubmit={this.handleSubmit} className="wrap">
                <label className="scrape">
                    <input autoFocus type="text" id="input" value={this.state.url} onChange={this.handleChange} placeholder="Input a university URL (e.g. https://www.illinois.edu)" className="scrapeBar" />
                    <button type="submit" className="scrapeButton">
                        {
                            this.state.loading ? <Puff /> : <FaSearch />
                        }
                    </button>
                </label>
            </form>
        ];
    }
}

export default FacultySearchBox;
