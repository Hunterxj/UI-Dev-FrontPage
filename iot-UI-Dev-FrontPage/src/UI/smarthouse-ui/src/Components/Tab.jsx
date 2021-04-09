import React, { Component } from "react";
import PropTypes from "prop-types";
import "../App.scss";

class Tab extends Component {
  static propTypes = {
    activeTab: PropTypes.string,
    label: PropTypes.string.isRequired,
    onClick: PropTypes.func,
  };

  onClick = () => {
    const { label, onClick } = this.props;
    onClick(label);
  };

  render() {
    const {
      onClick,
      props: { activeTab, label },
    } = this;

    let className = "tab-list-item";

    if (activeTab === label) {
      className += " tab-list-active";
    }

    return (
      <li className={className} onClick={onClick}>
        {label}
      </li>
    );
  }
}

export default Tab;