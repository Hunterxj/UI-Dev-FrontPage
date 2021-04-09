import React, { Component } from "react";
import PropTypes from "prop-types";
import "./LightBulb.css";


const STYLES = [   
  "btn--primary--solid",
  "btn--warning--solid",
  "btn--danger--solid",
  "btn--success--solid",
  "btn--primary--outline",
  "btn--warning--outline",
  "btn--danger--outline",
  "btn--success--outline"

]

const SIZES = ["btn--medium", "btn--small"];


export const LightBulb= ({children, type, onClick, 




}) => {


  return(
    <button onClick={onClick} type ={type}>

      {children}
    </button>
  )




};


export default LightBulb;
//class Lightbulb extends React.component {
  //  static propTypes = {
    //  lightOn: PropTypes.Boolean,
      //label: PropTypes.string.isRequired,
     // onClick: PropTypes.func,
    //};

    //render(){
        




    //}










//}