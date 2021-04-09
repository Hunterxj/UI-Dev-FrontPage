import { React, Component } from "react";
class StatusIndicatorComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      step: { answer: "" },
    };
    this.markAs = this.markAs.bind(this);
  }

  markAs() {
    this.setState({ step: { answer: "done" } });
  }

  render() {
    return (
      <StatusIndicatorComponent
        variant="raised"
        color={this.state.step.answer === "done" ? "primary" : "default"}
        onClick={this.markAs}
      >
        {" "}
        Done
      </StatusIndicatorComponent>
    );
  }
}

export default StatusIndicatorComponent;
