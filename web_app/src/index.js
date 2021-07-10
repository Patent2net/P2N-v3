import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";
import Requests from './pages/Requests';
import Request from './pages/Request/index';
import GetStarted from './pages/GetStarted';
import './index.css'
import Home from './pages/Home';
import DataIndex from './pages/DataIndex';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <nav className="bg-indigo-600 p-2 mt-0 w-full z-10 top-0 shadow text-white">
        <div className="container mx-auto flex flex-wrap items-center">
          <div className="flex w-full md:w-1/2 justify-center md:justify-start font-extrabold">
            <a className="no-underline hover:no-underline" href="/" >
              <span className="text-2xl pl-2"> Patent2Net</span>
            </a>
          </div>
          <div className="flex w-full pt-2 content-center justify-between md:w-1/2 md:justify-end">
            <ul className="list-reset flex justify-between flex-1 md:flex-none items-center">
              <li className="mr-3">
                <Link to="/app/"  className="inline-block no-underline hover:underline py-2 px-4">Home</Link>
              </li>
              
              <li className="mr-3">
                <Link to="/app/get_started" className="inline-block no-underline hover:underline py-2 px-4">Get Started</Link>
              </li>
              
              <li className="mr-3">
                <Link to="/app/requests"  className="inline-block py-2 px-4 no-underline font-medium">Requests</Link>
              </li>
              
              <li className="mr-3">
                <Link to="/app/index" className="inline-block no-underline hover:underline py-2 px-4">Index</Link>
              </li>
              
              <li className="mr-3">
                <a href="/downloadDat" className="inline-block no-underline hover:underline py-2 px-4">Download Data</a>
              </li>
              <li className="mr-3">
                <a href="/doc/_build/html/index.html" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-orange-500 hover:bg-white mt-4 lg:mt-0">Documentation</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      {/* A <Switch> looks through its children <Route>s and
          renders the first one that matches the current URL. */}
      <div className="my-10">
        <Switch>
          <Route path="/app/get_started">
            <GetStarted />
          </Route>
          <Route path="/app/requests/:dir">
            <Request />
          </Route>
          <Route path="/app/requests">
            <Requests />
          </Route>
          <Route path="/app/index">
            <DataIndex />
          </Route>
          <Route exact path="/app/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
