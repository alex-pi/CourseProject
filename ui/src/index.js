import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import FacultySearchBox from './faculty_scraper.js';
import Results from './results.js';
import { BrowserRouter, Route } from 'react-router-dom';

ReactDOM.render(
    <BrowserRouter basename={process.env.PUBLIC_URL}>
        <div>
            <Route exact path="/" component={FacultySearchBox} />
            <Route path="/results" component={Results} />
        </div>
    </BrowserRouter>,
    document.getElementById('root')
);
