import React from 'react';

const circleWidth = 10;

const GreenCircle = () => {
    return <div style={{ width: circleWidth, height: '10px', borderRadius: '50%', backgroundColor: 'green', display: 'inline-block' }}></div>;
};

const RedCircle = () => {
    return <div style={{ width: circleWidth, height: '10px', borderRadius: '50%', backgroundColor: 'red', display: 'inline-block' }}></div>;
};


const YellowCircle = () => {
    return <div style={{ width: circleWidth, height: '10px', borderRadius: '50%', backgroundColor: 'yellow', display: 'inline-block' }}></div>;
  };

export { GreenCircle, RedCircle, YellowCircle };