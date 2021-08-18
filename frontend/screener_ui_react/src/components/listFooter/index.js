





import React from 'react';
import './listFooter.css'
import PropTypes from 'prop-types';

import { FaSyncAlt } from 'react-icons/fa';





const Footer = props => {

    



    return (
        <div className="footer-container">
            <span>{`Last Updated: ${props.lastUpdated}`}</span>
            <FaSyncAlt
                onClick={props.refreshData}
                className="refresh-icon-button"/>
        </div>
    );
};

Footer.propTypes = {
    
};

export default Footer; 