import React from 'react'
import PropTypes from 'prop-types'
import { PageHeader, Label, Grid, Row, Col, Image } from 'react-bootstrap';

import { sisenseSettings } from './../config/sisense'
import Widget from './widget'

/*  Utility functions   */

const dropdownId = "sisense-dropdown";

function guid(){
  function S4() {
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1); 
  }
  return (S4() + S4() + "-" + S4() + "-4" + S4().substr(0,3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
}

function getDivId(oid){
  return "container-" + oid;
}

//  Function to check and see if Sisense.js has been loaded by another page
function sisenseIsLoaded(){
  return ((typeof window.Sisense !== "undefined") && (typeof window.prism !== "undefined"));
}

//  Function to get the dropdown menu components
function getDropdown(){

  //  For ESLint
  const $ = window.$;

  var container = $('#' + dropdownId).parent();
  var title = $('#' + dropdownId);
  var links = $('ul.dropdown-menu', container);

  return {
    'container': container,
    'title': title,
    'links': links
  }
}

/*  Sisense Dashboard component   */
class Dashboard extends React.Component {

  //  Component constructor
  constructor(props) {
    super(props);

    //  Initialize the component's state
    this.state = {
      "sisenseApp": null,
      "thisDashboard": null,
      "thisDashboardTitle": '',
      "widgets": [],
      "dashboards": [],
      "hasLoaded": false,
      "resetCounter": 0
    }

    //  Will allow `this` to work within the callbacks
    this.loadSisensejs = this.loadSisensejs.bind(this);
    this.getDashboards = this.getDashboards.bind(this);
    this.loadDashboard = this.loadDashboard.bind(this);
  }

  /*  Sisensejs initialization functions   */

  //  Step 1: Load the Sisense.js library
  loadSisensejs(){

    //  Check to see if Sisense.js has already been loaded
    var isLoaded = sisenseIsLoaded();
    if (!isLoaded){

      //  Create the new script tag
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = sisenseSettings.server + '/js/sisense.js?v=' + guid();
      script.async = true;

      //  Add an onload handler
      script.onload = function(){

        console.log("Sisense.js: Library Loaded");

        //  For ESLint
        const Sisense = window.Sisense;

        //  Callback for when the connect function is finished
        function connected(app){

          console.log("Sisense.js: Server Connected");

          //  Save a reference to the sisense app
          this.setState({
            'sisenseApp': app
          })
            
          //  Load the dashboard
          this.getDashboards();
        }

        //  Run the connect function, to establish a connection to your Sisense server
        Sisense.connect(sisenseSettings.server).then(connected.bind(this));

      }.bind(this)

      //  Add script to the body
      document.body.appendChild(script);
      
    } else {

      //  Load the dashboard
      this.getDashboards();
    }
  }

  //  Step 2: Get a list of dashboards from Sisense
  getDashboards(){

    //  Define the api call's url
    var url = sisenseSettings.server + '/api/v1/dashboards?fields=oid%2Ctitle';

    //  In order to make an API call to Sisense, we need a reference to $http
    var $http = this.state.sisenseApp.$$http;

    //  Callback function for the API call
    function processDashboards(response){

      //  Init a list of dashboards
      var dashboards = [];

      //  Find the dropdown menu on the page
      var dropdown = getDropdown();

      //  Clear the initial links
      dropdown.links.empty();

      //  Define a function to run on click of a dashboard
      function clicked(event) {

        //  For ESLint
        const $ = window.$;

        //  Get the selected dashboard id and title
        var oid = $(event.target).attr('rel');

        //  Close the dropdown menu
        $(event.target).closest('li.dropdown').removeClass('open')

        //  If a new dashboard was picked, load it
        if (this.state.thisDashboard.id !== oid) {
          this.loadDashboard(oid);
        }
        
      }
      
      //  Loop through each dashboard returned
      for (var dashboard of response.data){

        //  Figure out which dashboards match the criteria  
        var isValid = (dashboard.title.indexOf(sisenseSettings.dashboardTitlePrefix) === 0);
        if (isValid){

          //  Save to the state of this component
          dashboards.push(dashboard)

          //  Update the dropdown list, with menu options from the dashboard list
          var newLink = '<li role="presentation" class="">'
                        + '<a role="menuitem" tabindex="-1" href="#" rel="' + dashboard.oid + '">' 
                          + dashboard.title
                        + '</a>'
                      + '</li>';
          dropdown.links.append(newLink);
        }
      }

      //  Update the state
      this.setState({
        'dashboards': dashboards
      })

      //  Load the first dashboard returned
      var dashboardsCount = this.state.dashboards.length;
      if (dashboardsCount > 0) {

        //  Load the first dashboard by default
        this.loadDashboard(this.state.dashboards[0].oid);

        //  Add an event handler to the menu links
        dropdown.links.on('click', clicked.bind(this))
      }

      console.log("Sisense.js: Found " + dashboardsCount + " dashboards")

    }

    //  Run the API call
    $http.get(url).then(processDashboards.bind(this))
  }

  //  Step 3: Load the widgets from this dashboard
  loadDashboard(id){
    
    //  Callback for the loading of a dashboard
    function dashboardLoaded(dashboard){

      //  Initialize list of widgets
      var widgets = [];

      //  Loop through the widgets
      for (var widget of dashboard.widgets.$$widgets){

        //  Make sure this is not a blacklisted widget type
        var isValid = sisenseSettings.widgetTypesToExclude.indexOf(widget.type) < 0;
        if (isValid){

          //  Save a reference to the widget in the state
          widgets.push(widget)
        }
      }

      //  Update the state with a reference to the dashboard object 
      //  and a list of widgets.  This will trigger the render function,
      //  to add DIV containers for each widget.  Also, the componentDidUpdate
      //  function will run and render the widgets
      this.setState({
        thisDashboard: dashboard,
        thisDashboardTitle: dashboard.$$model.title,
        hasLoaded: true,
        widgets: []
      })

      //  This forces an old dashboard's widget components to be unmounted, 
      //  before rendering the new widgets
      function delay() {
        this.setState({
          widgets: widgets
        })
      }
      setTimeout(delay.bind(this),0)
    }

    //  Load the specific dashboard
    this.state.sisenseApp.dashboards.load(id).then(dashboardLoaded.bind(this))
  }

  /*  Component Handlers   */

  //  React handler, runs when the render process is finished
  componentDidMount(){

    //  Load the sisense.js library
    this.loadSisensejs();
  }

  //  Function that cleans up the resize event listener
  componentWillUnmount() {
  }

  //  Rendering function
  render() {

    //  Has a dashboard been loaded yet?
    let loading;
    if (!this.state.hasLoaded){
      //  Show a loading image, if Sisense.js is not yet loaded
      loading = <Row>
                  <Col className="loading">
                    <Label bsStyle="info">Loading</Label>
                    <br />
                    <Image src="/images/loading.gif"></Image>
                  </Col>
                </Row>;
    }

    return (
      <div className="sisenseDashboard">
        <PageHeader>
          <small>{this.state.thisDashboardTitle}</small>
        </PageHeader>
        <Grid fluid={true}>
          { loading }
          <Row>
            {
              //  Loop through each widget
              this.state.widgets.map(function(widget, index){

                //  Render a container for each
                return (<Widget key={widget.id} divId={getDivId(widget.id)} widget={widget}></Widget>)
              })
            }
          </Row>
        </Grid>
      </div>
    )
  }
}

Dashboard.propTypes = {
  'id': PropTypes.string,
}

export default Dashboard
