

import React from 'react';
import './loadingAnimation.css'
import PropTypes from 'prop-types';

import { FaSyncAlt } from 'react-icons/fa';

import Spinner from "react-svg-spinner";

const LoadingSpinner = () => {
    return (
        <div className="loading-spinner-container">
            <Spinner size="20px" color="white" /> 
        </div>
    );
};

export default LoadingSpinner;