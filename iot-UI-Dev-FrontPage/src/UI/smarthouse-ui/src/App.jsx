import * as React from "react";
import ReactDOM from "react-dom";
import TabButtonGroup from "./Components/TabButtonGroup";
import Tab from "./Components/Tab";
import { ReactComponent as FloorPlanSVG } from "./Icons/floor_plan.svg";
import { ReactComponent as LightBulboff } from "./Icons/lightbulb-off.svg";
import LightBulb from "./Components/LightBulb.jsx";
import "./App.scss";

class App extends React.Component {
  _isMounted = false;

  constructor(props) {
    super(props);
    this.state = {
      selected: "Home",
    };
  }
  setSelected = (tab) => {
    this.setState({ selected: tab });
  };

  //make an HTTP GET request to API
  componentDidMount() {
    this._isMounted = true;

    fetch("http://localhost:8000/api/v1/weather/all")
      .then((res) => res.json())
      .then((data) => {
        this.setState({ weather: data });
        console.log(data);
      })
      .catch(console.log);
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    return (
      <div
        className="App"
        style={{
          backgroundColor: "#eee",
          height: "100%",
          width: "100%",
          padding: "32px",
        }}
      >
        <TabButtonGroup
          tabs={["Devices", "Utility Stats", "Technician Panel"]}
          selected={this.state.selected}
          style={{
            backgroundColor: "#eee",
            height: "100%",
            width: "100%",
            padding: "32px",
          }}
        >
          <Tab label={"Devices"} isSelected={this.state.selected === "Devices"}>
            <div
              style={{
                height: "600px",
                width: "800px",
                backgroundColor: "#eee",
              }}
            >
              <FloorPlanSVG />
            </div>
            <div className="inner">

<input type="checkbox" name="lb" id="lb"/>
<label htmlFor="lb">
<div>
  
 <LightBulb onClick= {()=> {console.log("I have been clicked!")} }> <LightBulboff classname="lightBulboff"/></LightBulb>
  
  </div>
<span>Light On</span>
</label>

</div>
          </Tab>
          <Tab label={"Stats"} isSelected={this.state.selected === "Stats"}>
            <h1>Utility Usage Data</h1>
            <p>
              I'm out of time for now. Here's what you need to do. Consume API
              data here. You're probably going to want to use a library/module
              import like charts.js or whatever it's called. Use that to make a
              time series graph (stock market style graph) that conesumes API
              data from localhost:8000/api/v2/ PUTWHATEVER-ENDPOINTHERE
            </p>
          </Tab>
          <Tab
            i
            label={"Technician"}
            isSelected={this.state.selected === "Technician"}
          >
            <ul>
              <li>Beep Boop I'm a robot.</li>
              <li>
                Here's another randomly slapped together sentence for a list
                item.
              </li>
              <li>I hate React and Angular is better.</li>
            </ul>
          </Tab>
        </TabButtonGroup>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
export default App;